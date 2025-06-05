import os
from django.http import JsonResponse
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from django.views.decorators.csrf import csrf_exempt
import json

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

chat = ChatOpenAI(
  temperature=0.7,
  model_name="gpt-4o",
  openai_api_key=OPENAI_KEY
)

@csrf_exempt
def generate_carrousel_content(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    content = data.get('content')
    target_audience = data.get('target_audience')
    tone = data.get('tone')

    template = """
        You are a highly skilled copywriter specializing in social media content. Your task is to create:
        1) An Instagram carousel consisting of {num_slides} slides. Each slide should be clearly separated in Markdown format, with engaging visuals and concise text.
        2) A compelling description that captures the essence of the carousel and encourages user interaction.
        **Content Details:**
        - Content: {content}
        - Target Audience: {target_audience}
        - Tone of Voice: {tone}
        - Key Message: {key_message}
        **Instructions:**
        - Include a strong Call to Action (CTA) only on the first and last slides to guide user engagement.
        - The middle slides should focus on delivering valuable content and insights without CTAs, allowing the audience to absorb the information.
        **Example of Desired Output:**
        - Slide 1: [Title, Image Description, Call to Action]
        - Slide 2: [Title, Image Description]
        - Slide 3: [Title, Image Description]
        - Slide 4: [Title, Image Description]
        - Slide N: [Title, Image Description, Call to Action]
        Make sure to tailor the content to resonate with the target audience and reflect the specified tone.
        """

    prompt = PromptTemplate.from_template(template)

    response = chat.invoke(prompt.format(content=content, target_audience=target_audience, tone=tone))

    return JsonResponse({
      'carousel': response.content
    })

  return JsonResponse({'error': 'Invalid request method'}, status=400)