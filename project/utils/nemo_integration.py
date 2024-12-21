from typing import Dict, List
import torch
from nemo.collections.nlp.models import MegatronT5Model
from config.settings import NEMO_CONFIG

class NeMoModelManager:
    """Manages NeMo model loading and inference."""
    
    def __init__(self):
        self.model = self._load_model()
        
    def _load_model(self) -> MegatronT5Model:
        """Load and configure the NeMo model."""
        try:
            model = MegatronT5Model.from_pretrained(NEMO_CONFIG['model_name'])
            
            if NEMO_CONFIG['device'] == 'cuda':
                model = model.cuda()
                
            if NEMO_CONFIG['precision'] == 'fp16':
                model = model.half()
                
            return model
            
        except Exception as e:
            raise RuntimeError(f"Failed to load NeMo model: {str(e)}")

    def generate_code(self, prompt: str, max_length: int = 512) -> str:
        """Generate code using the NeMo model."""
        try:
            # Prepare input
            inputs = self.model.tokenizer.text_to_ids(prompt)
            inputs = torch.tensor([inputs]).to(self.model.device)
            
            # Generate
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                do_sample=True,
                top_p=0.95,
                top_k=50
            )
            
            # Decode
            generated_code = self.model.tokenizer.ids_to_text(outputs[0].tolist())
            return generated_code
            
        except Exception as e:
            raise RuntimeError(f"Code generation failed: {str(e)}")

    def analyze_code(self, code: str) -> Dict:
        """Analyze code for quality and potential issues."""
        try:
            # Prepare analysis prompt
            prompt = f"Analyze this code for issues:\n{code}"
            
            # Generate analysis
            analysis = self.generate_code(prompt, max_length=256)
            
            return {
                'analysis': analysis,
                'quality_score': self._calculate_quality_score(analysis)
            }
            
        except Exception as e:
            raise RuntimeError(f"Code analysis failed: {str(e)}")

    def _calculate_quality_score(self, analysis: str) -> float:
        """Calculate a quality score based on the analysis."""
        # Implement more sophisticated scoring logic
        score = 0.7  # Default score
        if 'error' in analysis.lower():
            score -= 0.2
        if 'good practice' in analysis.lower():
            score += 0.1
        return min(max(score, 0.0), 1.0) 