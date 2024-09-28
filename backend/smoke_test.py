from search import VectorSearch

bin_file_v2 = '/home/dinhln/Desktop/MLOPS/AIC/refactor/faiss_clipv2_cosine.bin'
json_path = '/home/dinhln/Desktop/MLOPS/AIC/refactor/image_paths_new.json'
cosine_faiss = VectorSearch(
#                        bin_clip_file=bin_file,
                       bin_clipv2_file=bin_file_v2,
                        json_path=json_path,
                        media_dir= "/home/dinhln/Desktop/MLOPS/AIC/refactor/media-info"
                   )

print(cosine_faiss.text_search("A duck ", None, 5, 'clipv2'))