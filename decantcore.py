#!/usr/bin/env python3
"""
DECANT v1.0 - Del caos, claridad
Transforma ideas desordenadas en esquemas estructurados.

USO:
    python decant.py
    Luego pega tu texto caótico y presiona Enter dos veces.

    O directamente:
    echo "tu texto caotico" | python decant.py
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

# ============================================================================
# MODELOS
# ============================================================================

class IdeaType(Enum):
    THESIS = "tesis"
    ARGUMENT = "argumento"
    EVIDENCE = "evidencia"
    OBJECTION = "objecion"
    EMOTION = "emocion"
    ACTION = "accion"
    CONTEXT = "contexto"

class FormatType(Enum):
    THREAD = "hilo_twitter"
    ESSAY = "ensayo"
    ARTICLE = "articulo"
    GUIDE = "guia_practica"

@dataclass
class Idea:
    texto: str
    tipo: IdeaType
    peso: float

# ============================================================================
# MOTOR PRINCIPAL
# ============================================================================

class Decant:
    
    def __init__(self):
        self.patterns = {
            IdeaType.THESIS: ['creo que', 'considero que', 'mi tesis es', 'la idea central', 'en esencia'],
            IdeaType.ARGUMENT: ['porque', 'ya que', 'dado que', 'debido a', 'la razón es', 'puesto que'],
            IdeaType.EVIDENCE: ['ejemplo', 'según', 'estudio', 'dato', 'investigación', 'caso', 'evidencia'],
            IdeaType.OBJECTION: ['pero', 'sin embargo', 'no obstante', 'el problema es', 'aunque', 'objeción'],
            IdeaType.EMOTION: ['me siento', 'odio', 'amo', 'frustra', 'entusiasma', 'preocupa', 'me gusta'],
            IdeaType.ACTION: ['hay que', 'podemos', 'sugiero', 'propongo', 'acción', 'concluyo', 'paso siguiente']
        }
    
    def _extract_ideas(self, text: str) -> List[Idea]:
        """Extrae y clasifica ideas del texto caótico"""
        # Limpiar y segmentar
        text = re.sub(r'\s+', ' ', text)
        sentences = re.split(r'[.!?;]+', text)
        sentences = [s.strip().lower() for s in sentences if len(s.strip()) > 10]
        
        ideas = []
        for sent in sentences:
            classified = False
            for tipo, keywords in self.patterns.items():
                if any(kw in sent for kw in keywords):
                    peso = 0.8 if any(kw in sent for kw in keywords[:2]) else 0.5
                    ideas.append(Idea(
                        texto=self._clean_sentence(sent),
                        tipo=tipo,
                        peso=peso
                    ))
                    classified = True
                    break
            if not classified:
                ideas.append(Idea(self._clean_sentence(sent), IdeaType.CONTEXT, 0.3))
        
        return sorted(ideas, key=lambda x: x.peso, reverse=True)
    
    def _clean_sentence(self, sent: str) -> str:
        """Limpia marcadores pero mantiene significado"""
        for kw in ['porque ', 'ya que ', 'creo que ', 'considero que ', 'sugiero ']:
            sent = sent.replace(kw, '')
        return sent[0].upper() + sent[1:]
    
    def _build_hierarchy(self, ideas: List[Idea]) -> Dict:
        """Construye jerarquía por tipo"""
        hierarchy = {
            'thesis': [], 'arguments': [], 'evidence': [],
            'objections': [], 'actions': [], 'context': []
        }
        for idea in ideas:
            if idea.tipo == IdeaType.THESIS:
                hierarchy['thesis'].append(idea)
            elif idea.tipo == IdeaType.ARGUMENT:
                hierarchy['arguments'].append(idea)
            elif idea.tipo == IdeaType.EVIDENCE:
                hierarchy['evidence'].append(idea)
            elif idea.tipo == IdeaType.OBJECTION:
                hierarchy['objections'].append(idea)
            elif idea.tipo == IdeaType.ACTION:
                hierarchy['actions'].append(idea)
            else:
                hierarchy['context'].append(idea)
        return hierarchy
    
    def _detect_format(self, hierarchy: Dict) -> FormatType:
        """Detecta automáticamente el mejor formato"""
        if len(hierarchy['actions']) > 2:
            return FormatType.GUIDE
        elif len(hierarchy['objections']) > 1:
            return FormatType.ESSAY
        elif len(hierarchy['arguments']) > 3:
            return FormatType.ARTICLE
        else:
            return FormatType.THREAD
    
    def _generate_title(self, hierarchy: Dict) -> str:
        """Genera título automático"""
        if hierarchy['thesis']:
            titulo = hierarchy['thesis'][0].texto[:50]
        elif hierarchy['actions']:
            titulo = hierarchy['actions'][0].texto[:50]
        else:
            titulo = "Decantación de ideas"
        return titulo.rstrip('.').strip()
    
    def transform(self, texto_caotico: str) -> Dict:
        """Método principal: transforma caos en estructura"""
        
        print("\n🧪 Decant: decantando ideas...")
        
        ideas = self._extract_ideas(texto_caotico)
        print(f"   → {len(ideas)} ideas extraídas")
        
        hierarchy = self._build_hierarchy(ideas)
        formato = self._detect_format(hierarchy)
        titulo = self._generate_title(hierarchy)
        
        print(f"   → Formato: {formato.value}")
        print(f"   → Título: {titulo}\n")
        
        # Generar outputs
        outputs = self._generate_outputs(hierarchy, formato, titulo)
        
        return outputs
    
    def _generate_outputs(self, hierarchy: Dict, formato: FormatType, titulo: str) -> Dict:
        
        # VERSIÓN EJECUTIVA
        ejecutivo = f"""╔════════════════════════════════════════════════════════════╗
║                    VERSIÓN EJECUTIVA                         ║
╚════════════════════════════════════════════════════════════╝

🎯 TESIS: {hierarchy['thesis'][0].texto if hierarchy['thesis'] else 'No detectada'}

⚠️  OBJECIÓN CLAVE: {hierarchy['objections'][0].texto if hierarchy['objections'] else 'Ninguna'}

✅ ACCIÓN PRIORITARIA: {hierarchy['actions'][0].texto if hierarchy['actions'] else 'No detectada'}

📊 RESULTADO: {len(hierarchy['arguments'])} argumentos | {len(hierarchy['evidence'])} evidencias
"""
        
        # VERSIÓN COMPLETA (según formato)
        completo = f"# {titulo}\n\n"
        
        if formato == FormatType.THREAD:
            completo += "🧵 HILO DE TWITTER\n\n"
            for i, arg in enumerate(hierarchy['arguments'][:5], 1):
                completo += f"{i}/🧵 {arg.texto}\n\n"
            if hierarchy['actions']:
                completo += f"🎯 {hierarchy['actions'][0].texto}\n\n"
            completo += "👇 ¿Qué opinas?"
            
        elif formato == FormatType.ESSAY:
            completo += "## 📌 Introducción\n"
            completo += f"{hierarchy['thesis'][0].texto if hierarchy['thesis'] else 'Exploración de ideas'}\n\n"
            completo += "## 🧠 Desarrollo\n"
            for i, arg in enumerate(hierarchy['arguments'][:3], 1):
                completo += f"### Argumento {i}\n{arg.texto}\n\n"
                # Buscar evidencia relacionada
                for ev in hierarchy['evidence']:
                    if any(word in ev.texto.lower() for word in arg.texto.lower().split()[:3]):
                        completo += f"*Evidencia:* {ev.texto}\n\n"
                        break
            if hierarchy['objections']:
                completo += "## ⚠️ Objeciones y réplicas\n"
                for obj in hierarchy['objections'][:2]:
                    completo += f"• {obj.texto}\n"
            completo += "## 🎯 Conclusión\n"
            completo += f"{hierarchy['actions'][0].texto if hierarchy['actions'] else 'Sintetizar los argumentos anteriores'}\n"
            
        elif formato == FormatType.ARTICLE:
            completo += f"> {hierarchy['thesis'][0].texto if hierarchy['thesis'] else 'Artículo'}\n\n"
            completo += "## Argumentos\n"
            for arg in hierarchy['arguments'][:3]:
                completo += f"**{arg.texto[:60]}**\n{arg.texto}\n\n"
            if hierarchy['evidence']:
                completo += "## Evidencias\n"
                for ev in hierarchy['evidence'][:2]:
                    completo += f"📊 {ev.texto}\n\n"
            if hierarchy['actions']:
                completo += "## Conclusión\n"
                completo += hierarchy['actions'][0].texto + "\n"
                
        else:  # GUIDE
            completo += "## 🎯 Objetivo\n"
            completo += f"{hierarchy['thesis'][0].texto if hierarchy['thesis'] else 'Completar la guía'}\n\n"
            completo += "## 📋 Pasos\n"
            for i, acc in enumerate(hierarchy['actions'][:5], 1):
                completo += f"### Paso {i}: {acc.texto[:40]}\n{acc.texto}\n\n"
            completo += "## ✅ Checklist\n"
            for acc in hierarchy['actions']:
                completo += f"- [ ] {acc.texto}\n"
        
        completo += "\n---\n*Decant - Del caos, claridad*"
        
        # TL;DR
        tldr = "╔════════════════════════════════════════════════════════════╗\n"
        tldr += "║                        TL;DR                              ║\n"
        tldr += "╚════════════════════════════════════════════════════════════╝\n\n"
        bullets = []
        if hierarchy['thesis']:
            bullets.append(f"🎯 {hierarchy['thesis'][0].texto[:70]}")
        if hierarchy['arguments']:
            bullets.append(f"💡 {hierarchy['arguments'][0].texto[:70]}")
        if hierarchy['actions']:
            bullets.append(f"✅ {hierarchy['actions'][0].texto[:70]}")
        while len(bullets) < 3:
            bullets.append(f"📌 Decant - Del caos, claridad")
        tldr += '\n'.join(bullets[:3])
        
        return {
            'ejecutivo': ejecutivo,
            'completo': completo,
            'tldr': tldr,
            'formato': formato.value,
            'titulo': titulo,
            'stats': {
                'ideas': len(hierarchy['thesis'] + hierarchy['arguments'] + hierarchy['evidence']),
                'argumentos': len(hierarchy['arguments']),
                'evidencias': len(hierarchy['evidence']),
                'acciones': len(hierarchy['actions'])
            }
        }

# ============================================================================
# INTERFAZ DE USUARIO
# ============================================================================

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                         DECANT v1.0                          ║
║                    Del caos, claridad                        ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    decant = Decant()
    
    print("Pega tu texto caótico (Enter dos veces para terminar):\n")
    
    lines = []
    empty_count = 0
    while True:
        try:
            line = input()
            if line == "":
                empty_count += 1
                if empty_count >= 2:
                    break
            else:
                empty_count = 0
            lines.append(line)
        except EOFError:
            break
    
    texto = '\n'.join(lines)
    
    if not texto.strip():
        print("\n❌ No ingresaste texto. Saliendo...")
        return
    
    resultado = decant.transform(texto)
    
    print("\n" + "="*70)
    print(resultado['ejecutivo'])
    
    print("\n" + "="*70)
    print("📄 VERSIÓN COMPLETA")
    print("="*70)
    print(resultado['completo'])
    
    print("\n" + "="*70)
    print(resultado['tldr'])
    
    print("\n" + "="*70)
    print("📊 ESTADÍSTICAS")
    print("="*70)
    for k, v in resultado['stats'].items():
        print(f"  • {k}: {v}")
    print(f"  • formato: {resultado['formato']}")
    
    # Guardar archivo
    filename = f"decant_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(resultado['completo'])
    print(f"\n💾 Guardado: {filename}")

if __name__ == "__main__":
    main()