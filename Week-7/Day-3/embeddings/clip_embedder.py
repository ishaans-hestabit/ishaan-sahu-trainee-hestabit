import open_clip
import torch
from PIL import Image


class CLIPEmbedder:
    def __init__(self):
        self.model, _, self.preprocess = open_clip.create_model_and_transforms( 'ViT-B-32', pretrained='openai')
        self.tokenizer = open_clip.get_tokenizer('ViT-B-32')
        self.model.eval()  
        print("[CLIPEmbedder] Ready.")

    def embed_image(self, image: Image.Image) -> list:

        tensor = self.preprocess(image).unsqueeze(0) 
        with torch.no_grad():
            emb = self.model.encode_image(tensor)
            emb = emb / emb.norm(dim=-1, keepdim=True)  
        return emb.squeeze().tolist()

    def embed_text(self, text: str) -> list:
        tokens = self.tokenizer([text])
        with torch.no_grad():
            emb = self.model.encode_text(tokens)
            emb = emb / emb.norm(dim=-1, keepdim=True)
        return emb.squeeze().tolist()