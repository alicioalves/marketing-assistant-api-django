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
        You are a specialized copywriter. Generate:
        1) An Instagram carousel. Return the response in Markdown, clearly separating the slides of the carousel.
        2) An excellent description.
        content: {content}
        Target audience: {target_audience}
        Tone: {tone}
        """

    prompt = PromptTemplate.from_template(template)

    response = chat.invoke(prompt.format(content=content, target_audience=target_audience, tone=tone))

    return JsonResponse({
      'carousel': response.content
    })

  return JsonResponse({'error': 'Invalid request method'}, status=400)