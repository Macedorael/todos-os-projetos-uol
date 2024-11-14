# Importando os intents
from .agendar import agendar_intent
from .cancelar import cancelar_intent
from .verificar import verificar_intent
from .saudacoes import saudacoes_intent
from .valores import valores_intent

from .lambda_function import get_audio_url_from_tts, all_slots_filled
