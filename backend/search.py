import re
import os
import clip
import open_clip
import torch
import json
import glob
import faiss
import numpy as np
from .translate import Translation
from .config import ClipConfig

class VectorSearch:
    def __init__(self, bin_clipv2_file: str, json_path: str, media_dir:str):    

        self.index_clipv2 = self.load_bin_file(bin_clipv2_file)
        
        self.id2img_fps = self.load_json_file(json_path)
        self.media_dir = media_dir
        self.translater = Translation()
        self.__device = ClipConfig.device
        # self.clip_model, _ = clip.load(ClipConfig.clip_model, device=self.__device)

        print("Loading CLIP model...")
        self.clipv2_model, _, _ = open_clip.create_model_and_transforms(ClipConfig.clipv2_model, device=self.__device, pretrained=ClipConfig.clipv2_pretrained)
        self.clipv2_tokenizer = open_clip.get_tokenizer(ClipConfig.clipv2_model)

    def load_json_file(self, json_path: str):
        with open(json_path, 'r') as f: 
            js = json.load(f)
        return {int(k):v for k,v in js.items()}
    
    def load_bin_file(self, bin_file: str):
        return faiss.read_index(bin_file)

    def text_search(self, text, index, k, model_type):
        """
        Perform a text-based search on the given index.
        Args:
            text (str): The text to search for.
            index (faiss.Index): The index to search on.
            k (int): The number of nearest neighbors to retrieve.
            model_type (str): The type of model to use for encoding text.
        Returns:
            tuple: A tuple containing the following elements:
                - scores (numpy.ndarray): The similarity scores of the retrieved images.
                - idx_image (numpy.ndarray): The indices of the retrieved images.
                - infos_query (list): A list of dictionaries containing information about the retrieved images.
                - image_paths (list): A list of paths to the retrieved images.
                - ranked_image_paths (list): A list of paths to the retrieved images after reranking.
                - metadata (list): A list of metadata corresponding to the ranked images.
        """
        text = self.translater(text)

        ###### TEXT FEATURES EXTRACTING ######
        if model_type == 'clip':
            text = clip.tokenize([text]).to(self.__device)  
            text_features = self.clip_model.encode_text(text)
        else:
            text = self.clipv2_tokenizer([text]).to(self.__device)  
            text_features = self.clipv2_model.encode_text(text)
        
        text_features /= text_features.norm(dim=-1, keepdim=True)
        text_features = text_features.cpu().detach().numpy().astype(np.float32)

        ###### SEARCHING #####
        if model_type == 'clip':
#             index_choosed = self.index_clip
            pass
        else:
            index_choosed = self.index_clipv2
        
        if index is None:
            scores, idx_image = index_choosed.search(text_features, k=k)
            
        else:
            id_selector = faiss.IDSelectorArray(index)
            scores, idx_image = index_choosed.search(text_features, k=k, 
                                                   params=faiss.SearchParametersIVF(sel=id_selector))
        idx_image = idx_image.flatten()
        # Rerank the images based on text similarity
        ranked_indices, rerank_scores = self.rerank_images(torch.tensor(text_features, device=self.__device), idx_image)

        # Get the corresponding image paths after reranking
        ranked_image_paths = [self.id2img_fps[idx_image[i]]['image_path'] for i in ranked_indices]
        # Read the metadata from the json files
        # print(ranked_image_paths)
        metadata = {}
        for path in ranked_image_paths:
            field = path.split('/')
            json_path = os.path.join(self.media_dir, f"{field[-3]}_{field[-2].split('_')[-1]}.json")
            with open(json_path, 'r') as f:
                info = json.load(f)
            second = round(int(field[-1].split('.')[-2])/25)
            metadata[path] = info["watch_url"]+ f"?v=VIDEO_ID&t={second}s"

        ###### GET INFOS KEYFRAMES_ID ######
        infos_query = list(map(self.id2img_fps.get, list(idx_image)))
        image_paths = [info['image_path'] for info in infos_query]

        return scores.flatten(), idx_image, infos_query, image_paths, ranked_image_paths, metadata

    def rerank_images(self, text_features, idx_image):
        """
        Rerank images based on similarity to the provided text features.

        Parameters:
        - text_features: The encoded features of the text query.
        - idx_image: The indices of images retrieved from the initial search.

        Returns:
        - ranked_indices: A list of indices ranked by similarity to the text query.
        - similarity_scores: The similarity scores for the ranked frames.
        """
        # Reconstruct the image features from the FAISS index using idx_image
        image_features = np.vstack([self.index_clipv2.reconstruct(int(idx)) for idx in idx_image])

        # Convert to torch tensor and move to the appropriate device
        image_features = torch.tensor(image_features, device=self.__device)

        # Normalize the image features
        image_features /= image_features.norm(dim=-1, keepdim=True)

        # Compute similarity scores between the text features and reconstructed image features
        similarity_scores = (image_features @ text_features.T).squeeze(1)

        # Rank the images based on the similarity scores
        ranked_indices = similarity_scores.argsort(descending=True).cpu().numpy()

        return ranked_indices, similarity_scores.cpu().numpy()
   
        