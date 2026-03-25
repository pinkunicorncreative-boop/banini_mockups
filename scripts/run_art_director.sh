#!/bin/bash
export BNNI_API_KEY="bnni_WFvLygMU9wGeQQD0QNOXX5GgrMakMHYw"
claude mcp add banani npx -y @banani/mcp-server --api-key $BNNI_API_KEY || true

claude -p "You are the UI/UX Art Director Agent for Krazee Rasta Group (specifically the Jamrock brand). We have a new tool: Banani MCP. Use your Banani MCP tools to generate a high-fidelity, immersive e-commerce homepage mockup for 'Jamrock'. 

Vibe & Color Palette: Deep blacks, cream highlights, and muted neutral tones. Cinematic realism. Texture over gloss. ABSOLUTELY NO tourist tropes, no bright flag colors, no noisy embellishments. The aesthetic must feel like a luxury fashion house telling a cultural story.

UI Architecture:
1. The Hero (The Umbrella): Full-bleed, edge-to-edge cinematic video container. Bold, authoritative, heavy sans-serif typography overlay centered. Headline: 'NUH APOLOGIES.' Subtext: 'The culture, uncompromised. Cinematic storytellers of the diaspora.' Minimalist, transparent sticky nav bar.
2. The Manifesto Block: Asymmetric split screen. Left side: Heavy, dignified editorial text about wearing the culture with elevated, everyday style. Right side: Tall, medium-format style portrait. Dignified, powerful posture.
3. The Artifacts (Shop Grid): Clean, 3-column masonry or strict grid product layout. High-end fashion spacing. Lots of negative space.
4. Campaign Gateway (The Cinema): A wide, letterboxed cinematic video thumbnail section introducing current campaigns (e.g., 'Chapter 01: They Carried It').

UI chrome (buttons, borders) must be nearly invisible. Let the photography and typography carry the absolute weight of the page.

Generate this mockup using Banani, and output the final preview link."
