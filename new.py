

import marimo

__generated_with = "0.12.8"
app = marimo.App(width="medium", layout_file="layouts/new.slides.json")


@app.cell
def _():
    # Cell 1: Imports & Setup
    import json
    import os
    from typing import Optional

    import httpx
    import marimo as mo
    from dotenv import load_dotenv

    load_dotenv()
    # We'll keep a response cache to avoid regenerating the same prompts:
    response_cache = {}
    return Optional, httpx, json, mo, os


@app.cell
def _(mo):
    # Cell 2: Define custom CSS with our new style
    def custom_css():
        return mo.md("""
        <style>
        /* Import Bebas Neue font for headings */
        @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap');
        /* Import Inter font for body text */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;700&display=swap');

        body {
            background-color: #F9F7F4;
            color: #000;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Bebas Neue', Helvetica, Arial, sans-serif !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            color: #000000;
        }

        p, li, span {
            font-family: 'Inter', sans-serif;
        }

        .technique-header {
            border-bottom: 2px solid #9D0208 !important;
            background-color: #F9F7F4 !important;
            padding: 30px 0 !important;
        }

        .red-border {
            border-left: 3px solid #D00000 !important;
        }

        .red-accent {
            color: #D00000 !important;
            letter-spacing: 5px !important;
        }

        .btn-primary {
            background-color: #E5383B !important;
            color: #FFFFFF !important;
            border: 2px solid #9D0208 !important;
            padding: 15px 10px !important;
            font-size: 18px !important;
            font-weight: bold !important;
            text-transform: uppercase !important;
            letter-spacing: 2px !important;
            cursor: pointer !important;
        }

        .dark-section {
            background-color: #000000 !important;
            color: #FFFFFF !important;
            border: 2px solid #9D0208 !important;
            padding: 40px 30px !important;
        }
        </style>
        """)


    return (custom_css,)


@app.cell
def _(Optional, httpx, json, os):
    # Cell 3: DirectLLMClient Implementation
    class DirectLLMClient:
        """A direct HTTP client for LLM APIs that bypasses Marimo's implementations."""

        def __init__(self, provider: str = 'openai'):
            """
            Initialize the LLM client.

            Args:
                provider: The LLM provider to use ('openai', 'anthropic', etc.)
            """
            self.provider = provider.lower()
            self.client = httpx.Client(timeout=60.0)  # Generous timeout for LLM responses

            # Set up headers and endpoints based on provider
            if self.provider == 'openai':
                self.api_key = os.environ.get('OPENROUTER_API_KEY')
                if not self.api_key:
                    raise ValueError('OPENROUTER_API_KEY environment variable not set')
                self.headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key}',
                }
                self.endpoint = 'https://openrouter.ai/api/v1/chat/completions'
                self.default_model = 'openai/gpt-4o-mini'

            elif self.provider == 'anthropic':
                self.api_key = os.environ.get('ANTHROPIC_API_KEY')
                if not self.api_key:
                    raise ValueError('ANTHROPIC_API_KEY environment variable not set')
                self.headers = {
                    'Content-Type': 'application/json',
                    'x-api-key': self.api_key,
                    'anthropic-version': '2023-06-01',
                }
                self.endpoint = 'https://api.anthropic.com/v1/messages'
                self.default_model = 'claude-3-haiku-20240307'

            else:
                raise ValueError(f'Unsupported provider: {provider}')

        def generate(
            self,
            prompt: str,
            system_message: str = 'You are a helpful assistant.',
            model: Optional[str] = None,
            temperature: float = 0.7,
        ) -> str:
            """
            Generate a response from the LLM.

            Args:
                prompt: The user's input prompt
                system_message: System message to guide the model
                model: Model name to use (provider-specific)
                temperature: Temperature parameter for generation

            Returns:
                The model's response as a string
            """
            model = model or self.default_model

            try:
                if self.provider == 'openai':
                    payload = {
                        'model': model,
                        'messages': [
                            {'role': 'system', 'content': system_message},
                            {'role': 'user', 'content': prompt},
                        ],
                        'temperature': temperature,
                    }

                    response = self.client.post(self.endpoint, headers=self.headers, json=payload)

                    response.raise_for_status()
                    data = response.json()
                    return data['choices'][0]['message']['content']

                if self.provider == 'anthropic':
                    payload = {
                        'model': model,
                        'system': system_message,
                        'messages': [{'role': 'user', 'content': prompt}],
                        'temperature': temperature,
                        'max_tokens': 1000,  # Adding this as it's required by newer API versions
                    }

                    # Add debugging to see what's happening
                    print(f'Sending request to: {self.endpoint}')
                    print(f'Headers: {json.dumps(self.headers, indent=2)}')
                    print(f'Payload: {json.dumps(payload, indent=2)}')

                    response = self.client.post(self.endpoint, headers=self.headers, json=payload)

                    response.raise_for_status()
                    data = response.json()
                    return data['content'][0]['text']

            except httpx.HTTPError as e:
                return f'Error making request: {str(e)}'
            except KeyError as e:
                return f'Unexpected response format: {str(e)}'
            except Exception as e:
                return f'Unexpected error: {str(e)}'
    return (DirectLLMClient,)


@app.cell
def _(mo):
    get_submissions, set_submissions = mo.state([])
    get_prompt, set_prompt = mo.state('')
    return


@app.cell
def _(custom_css, mo):
    # Cell 4: Create state variables
    custom_css()
    language_is_english = mo.ui.checkbox(label='Before we start, check the box for English! Click on the corners for tthe next or previous page / Clique nos cantos para a próxima página ou anterior', value=False)
    language_is_english
    return (language_is_english,)


@app.cell
def _(language_is_english):
    def get_current_language():
        """Returns 'en' if language switch is set to English, otherwise 'pt'."""
        return 'en' if language_is_english.value else 'pt'
    return (get_current_language,)


@app.cell
def _():
    # Cell 5: Translations Dictionary
    translations = {
        'language_toggle': {'en': 'LANGUAGE', 'pt': 'IDIOMA'},
        'english': {'en': 'ENGLISH', 'pt': 'INGLÊS'},
        'portuguese': {'en': 'PORTUGUESE', 'pt': 'PORTUGUÊS'},
        'welcome_title': {
            'en': 'PROMPTING TECHNIQUES INTERACTIVE EXERCISES',
            'pt': 'EXERCÍCIOS INTERATIVOS DE TÉCNICAS DE PROMPT',
        },
        'welcome_description': {
            'en': "This notebook demonstrates prompting techniques using Marimo and Anthropic's Claude model.",
            'pt': 'Este notebook demonstra técnicas de prompt usando Marimo e o modelo Claude da Anthropic.',
        },
        'issue': {'en': 'ISSUE', 'pt': 'PROBLEMA'},
        'examples': {'en': 'EXAMPLES', 'pt': 'EXEMPLOS'},
        'without_technique': {'en': 'WITHOUT TECHNIQUE', 'pt': 'SEM A TÉCNICA'},
        'with_technique': {'en': 'WITH TECHNIQUE', 'pt': 'COM A TÉCNICA'},
        'prompt': {'en': 'PROMPT', 'pt': 'PROMPT'},
        'get_response': {'en': 'GET RESPONSE', 'pt': 'OBTER RESPOSTA'},
        'generating': {'en': 'GENERATING RESPONSE...', 'pt': 'GERANDO RESPOSTA...'},
        'response': {'en': 'RESPONSE:', 'pt': 'RESPOSTA:'},
        'explanation': {'en': 'WHY THIS WORKS BETTER', 'pt': 'POR QUE ISSO FUNCIONA MELHOR'},
        'why_it_works': {'en': 'WHY THIS TECHNIQUE WORKS', 'pt': 'POR QUE ESTA TÉCNICA FUNCIONA'},
        'additional_resources': {'en': 'ADDITIONAL RESOURCES', 'pt': 'RECURSOS ADICIONAIS'},
        'chat_experiment': {'en': 'TRY IT YOURSELF', 'pt': 'EXPERIMENTE VOCÊ MESMO'},
        'your_prompt': {'en': 'YOUR PROMPT', 'pt': 'SEU PROMPT'},
        'enter_prompt_here': {'en': 'ENTER YOUR PROMPT HERE...', 'pt': 'DIGITE SEU PROMPT AQUI...'},
        'inject_bad_prompt': {'en': 'USE BAD PROMPT', 'pt': 'USAR PROMPT RUIM'},
        'inject_good_prompt': {'en': 'USE GOOD PROMPT', 'pt': 'USAR PROMPT BOM'},
        'send_prompt': {'en': 'SEND PROMPT', 'pt': 'ENVIAR PROMPT'},
        'table_of_contents': {'en': 'TABLE OF CONTENTS', 'pt': 'ÍNDICE'},
        'using_api_key': {
            'en': '✓ USING ANTHROPIC API KEY FROM ENVIRONMENT',
            'pt': '✓ USANDO CHAVE DE API DA ANTHROPIC DO AMBIENTE',
        },
        'enter_api_key': {
            'en': 'ENTER YOUR ANTHROPIC API KEY',
            'pt': 'DIGITE SUA CHAVE DE API DA ANTHROPIC',
        },
        'api_key_placeholder': {
            'en': 'ENTER YOUR API KEY HERE',
            'pt': 'DIGITE SUA CHAVE DE API AQUI',
        },
    }
    return (translations,)


@app.cell
def _(mo):
    mo.md(
        """
        <div style="display: flex; flex-direction: column; align-items: center; padding: 30px 0; position: relative; border-bottom: 2px solid #9D0208; background: #F9F7F4; width: 100%; box-sizing: border-box;">
            <div style="position: relative; width: 100%; display: flex; flex-direction: column; align-items: center; padding: 0 20px">
                <!-- Removed the "LEGAL AI ENGINEERING" div as it contained new words -->
                <h1 style="font-size: 64px; font-weight: bold; margin: 0; text-align: center; letter-spacing: 2px; text-transform: uppercase; line-height: 1; color: #000; padding: 10px; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif;">
                    Prompting Techniques for Attorneys
                </h1>
                <div style="font-size: 20px; margin-top: 15px; color: #333; text-align: center; font-family: 'Inter', sans-serif;">
                    Learn how to craft effective prompts for AI language models
                </div>
                <div style="width: 50px; height: 5px; background: #9D0208; margin: 20px 0"></div>
                <div style="display: flex; align-items: center">
                    <div style="width: 30px; height: 2px; background: #E5383B"></div>
                    <div style="padding: 0 10px; font-size: 16px; color: #333; font-family: 'Inter', sans-serif;">
                        By <a href="https://synthetic.lawyer" style="color: inherit; text-decoration: none;">Arthur Souza Rodrigues</a>
                    </div>
                    <div style="width: 30px; height: 2px; background: #E5383B"></div>
                </div>
            </div>
        </div>
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        <div style="padding: 40px 30px; background: #fff; font-family: 'Inter', sans-serif;">
            <div style="display: flex; align-items: flex-start; gap: 30px">
                <div style="flex: 1; border-left: 3px solid #D00000; padding-left: 20px">
                    <h2 style="font-size: 36px; font-weight: bold; margin: 0 0 20px 0; text-transform: uppercase; letter-spacing: 1px; color: #000; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif;">
                        Welcome!
                    </h2>
                    <p style="font-family: 'Inter', sans-serif; font-size: 16px; line-height: 1.6; margin-bottom: 20px; color: #333">
                        <strong>Hey there!</strong><br/>
                        I know, I know, you already regret clicking this link. But you can't resist the temptation to procrastinate. I'm giving you an excellent reason, please be thankful.<br/><br/>
                        This is an ✨interactive✨ notebook, split in err... too many lessons. The goal is to dig in a bit more, so you can pretend (like me), that you really studied hard all those papers and understand the reason behind the format. The same level of our bar exam preparation course (10 years for me, ouch!).<br/><br/>
                        You will have a general rule, a use-case, then an example of a bad and a good prompt. Then why the good is good or amazing, or less bad.<br/><br/>
                        Then, if you reeeeeally want to spend your time, we have two clickable accordions (the thingy below the tabs), one giving more information and the other providing theoretical or experience support.
                    </p>
                    <p style="font-family: 'Inter', sans-serif; font-size: 16px; line-height: 1.6; margin-bottom: 20px; color: #333">
                        Each technique comes with real-world examples of what works, what flops, and why. By the end, you'll be extracting genuinely useful legal analysis instead of whatever that thing is the AI usually gives you on the first try. Or maybe you will get even worse results, I can't guarantee.<br/><br/>
                        Also, to torture you well tortured souls, after each section you will be able to test your ✨deepmind deepknowledge deepresearch✨ mind.<br/><br/>
                        In all seriousness, I'm confident this will be useful to you and I hope it actually is!<br/><br/>
                        Best,<br/>Arthur<br/><br/>
                        Ps. Hey! If you read this, follow me on <a href="https://www.linkedin.com/in/arthrod/detail/recent-activity/" style="color: #4267B2; text-decoration: none;">LinkedIn</a>, pretty please?<br/>
                        Ps2. Yes, Claude corrected me on 'Le Gran Finale.' But just to prove that I wrote this myself (I mean, kind off), I decided to leave as is.
                    </p>
                </div>
                <div style="flex: 1; border-right: 3px solid #D00000; padding-right: 20px">
                    <div style="background: #F5CAC3; padding: 25px; margin-bottom: 20px">
                        <h3 style="font-size: 24px; margin: 0 0 15px 0; color: #9D0208; text-transform: uppercase; letter-spacing: 1px; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif;">
                            What You'll Learn Today:
                        </h3>
                        <ol style="padding: 0 0 0 20px; margin: 0; font-family: 'Inter', sans-serif; color: #333">
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Role-Based Prompts</span> - Make the AI think it graduated top of its class at Harvard Law
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Context-Rich Instructions</span> - Because models can't read your mind (yet!)
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Constraint-Based Commands</span> - For when you want JUST the termination clause, not the entire 50-page agreement
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Example-Driven Templates</span> - Show, don't tell (just like that partner who never explains what they want)
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Step-by-Step Legal Analysis</span> - Force the AI to show its work like your 1L professor
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Contract Extraction Wizardry</span> - Getting the needle from the haystack without the haystack
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">MSA Clause Drafting</span> - Making clauses that won't make your GC cry
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Ambiguity Handling</span> - Because legal language is confusing (on purpose!)
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Comparative Law Techniques</span> - For when one jurisdiction isn't complicated enough
                            </li>
                            <li style="margin-bottom: 10px">
                                <span style="color: #000; font-weight: bold">Le Gran Finale</span> - The SURPRISE technique! Placing critical instructions at the end ...
                            </li>
                        </ol>
                    </div>
                </div>
            </div>
        </div>
        """
    )
    return


@app.cell
def _():
    # Cell 7: Technique Data
    technique1_slug = 'persona'
    technique1_name = {
        "en": "Role-Based Prompting (Persona Priming)",
        "pt": "Prompting Baseado em Papéis (Preparação de Persona)",
    }
    technique1_description = {
        "en": "Role-based prompting involves explicitly assigning the AI a specific role or persona relevant to the task. For example, you might begin a prompt with \"You are an experienced contracts attorney…\" or \"Act as a judge writing an opinion…\". This primes the model to adopt the perspective, knowledge, and tone of that role. It can also include defining the audience or viewpoint (e.g. \"explain like I'm a client\" vs. \"write as a legal scholar\"). By setting a persona, the prompt guides the LLM to produce answers aligned with that expertise or viewpoint.",
        "pt": "O prompting baseado em papéis envolve atribuir explicitamente à IA um papel ou persona específica relevante para a tarefa. Por exemplo, você pode começar um prompt com \"Você é um advogado experiente em contratos...\" ou \"Atue como um juiz escrevendo uma opinião...\". Isso prepara o modelo para adotar a perspectiva, conhecimento e tom desse papel. Também pode incluir a definição do público ou ponto de vista (ex: \"explique como se eu fosse um cliente\" vs. \"escreva como um estudioso do direito\"). Ao definir uma persona, o prompt orienta o LLM a produzir respostas alinhadas com essa expertise ou ponto de vista.",
    }
    technique1_why_it_works = {
        "en": "Specifying a role focuses the LLM on domain-specific knowledge and style, narrowing the scope of its response. Authoritative guidance suggests treating the LLM \"as a brilliant but very new employee…who needs explicit instructions,\" which includes giving it a clear role. Research has shown that responses can improve in accuracy when the prompt asks for analysis in the voice of a particular expert; for instance, GPT-4 gave a correct answer when asked to analyze a case \"as [Harvard Law Professor] Cass Sunstein might,\" whereas a generic prompt yielded a hallucination. In practice, a persona provides context that the model can implicitly use (such as legal terminology or methodology familiar to that role), resulting in more on-point and technically accurate answers.",
        "pt": "Especificar um papel concentra o LLM em conhecimentos e estilos específicos do domínio, restringindo o escopo de sua resposta. Orientações autoritativas sugerem tratar o LLM \"como um funcionário brilhante, mas muito novo... que precisa de instruções explícitas\", o que inclui dar-lhe um papel claro. Pesquisas demonstraram que as respostas podem melhorar em precisão quando o prompt solicita análise na voz de um especialista específico; por exemplo, o GPT-4 deu uma resposta correta quando solicitado a analisar um caso \"como [o Professor de Direito de Harvard] Cass Sunstein faria\", enquanto um prompt genérico produziu uma alucinação. Na prática, uma persona fornece contexto que o modelo pode usar implicitamente (como terminologia jurídica ou metodologia familiar àquele papel), resultando em respostas mais precisas e tecnicamente acuradas.",
    }
    technique1_example_question = {
        "en": "A client's supplier breached a contract. What should the client do?",
        "pt": "O fornecedor de um cliente violou um contrato. O que o cliente deve fazer?",
    }
    technique1_example_bad_prompt = {
        "en": "What should a company do if a supplier breaks a contract?",
        "pt": "O que uma empresa deve fazer se um fornecedor quebrar um contrato?",
    }
    technique1_example_good_prompt = {
        "en": "You are a seasoned contracts attorney advising a tech company. The company's supplier failed to deliver goods, breaching their contract. Explain the legal steps the company should take next (e.g. sending a breach notice, seeking damages under the contract or UCC), in plain language for a business executive.",
        "pt": "Você é um advogado experiente em contratos assessorando uma empresa de tecnologia. O fornecedor da empresa não entregou os produtos, violando o contrato. Explique os passos legais que a empresa deve tomar a seguir (por exemplo, enviar uma notificação de violação, buscar indenização conforme o contrato ou o Código Comercial), em linguagem simples para um executivo de negócios.",
    }
    technique1_example_explanation = {
        "en": "By assigning the AI the role of a \"seasoned contracts attorney,\" the model focuses on providing legally sound advice about contract breaches. The prompt also specifies the audience (a business executive), which guides the AI to use \"plain language\" while still covering technical legal concepts like breach notices and UCC remedies. The resulting response is likely to include structured legal steps, appropriate citations to relevant law, and practical advice—all delivered in the professional tone of an attorney advising a client. Without this role priming, the response might lack legal specificity or fail to address formal remedies available under contract law.",
        "pt": "Ao atribuir à IA o papel de um \"advogado experiente em contratos\", o modelo se concentra em fornecer orientações juridicamente sólidas sobre violações contratuais. O prompt também especifica o público (um executivo de negócios), o que orienta a IA a usar \"linguagem simples\" enquanto ainda aborda conceitos jurídicos técnicos como notificações de violação e remédios previstos em lei comercial. A resposta resultante provavelmente incluirá etapas legais estruturadas, citações apropriadas à legislação relevante e conselhos práticos—tudo entregue no tom profissional de um advogado orientando um cliente. Sem essa preparação de papel, a resposta poderia carecer de especificidade jurídica ou deixar de abordar os remédios formais disponíveis sob a lei contratual.",
    }
    technique1_resource_title = {
        "en": "GenAI Prompting Tips for Lawyers",
        "pt": "Dicas de Prompting com IA Generativa para Advogados",
    }
    technique1_resource_url = 'https://cl.cobar.org/departments/genai-prompting-tips-for-lawyers/'
    technique1_resource_description = {
        "en": "Comprehensive guide on effective prompting techniques for legal professionals",
        "pt": "Guia abrangente sobre técnicas eficazes de prompting para profissionais jurídicos",
    }
    return


@app.cell
def _():
    # Cell: Technique 2 Definition
    technique2_slug = 'context-rich'
    technique2_name = {
        "en": "Context-Rich Prompting (Including Details and Background)",
        "pt": "Prompting com Contexto Rico (Incluindo Detalhes e Antecedentes)",
    }
    technique2_description = {
        "en": "Context-rich prompting means supplying the LLM with all relevant background facts, documents, and parameters of the query. Rather than asking a question in isolation, you include essential details such as the jurisdiction, involved parties, key facts, and the specific legal issue at hand. For instance, instead of \"Can I fire an employee for social media posts?\", you would ask, \"As an employer in California, can I lawfully fire an at-will employee who posted negative comments about our company on social media?\". You might also provide the text of a law or contract clause if interpretation is needed. By giving this specific context, you reduce ambiguity and guide the AI to consider the correct factual and legal framework.",
        "pt": "O prompting com contexto rico significa fornecer ao LLM todos os fatos relevantes de antecedentes, documentos e parâmetros da consulta. Em vez de fazer uma pergunta isolada, você inclui detalhes essenciais como a jurisdição, as partes envolvidas, fatos-chave e a questão jurídica específica em questão. Por exemplo, em vez de \"Posso demitir um funcionário por postagens em redes sociais?\", você perguntaria: \"Como empregador em São Paulo, posso legalmente demitir um funcionário CLT que publicou comentários negativos sobre nossa empresa nas redes sociais?\". Você também pode fornecer o texto de uma lei ou cláusula contratual se for necessária interpretação. Ao fornecer esse contexto específico, você reduz a ambiguidade e orienta a IA a considerar o quadro factual e jurídico correto.",
    }
    technique2_why_it_works = {
        "en": "Context is a primary driver of LLM performance. Extensive user research shows that specific context helps the LLM identify the correct laws, facts, and analysis to apply. When the LLM has access to relevant law and facts, the model grounds its analysis in the proper legal framework and avoids introducing irrelevant factors. This leads to answers that address the actual issue at hand, rather than defaulting to generic statements about the law. Providing geographical context (e.g., jurisdiction) is particularly important, as laws vary significantly between states and countries. Even if LLMs know the law in theory, they're more likely to default to general interpretations without specific context.",
        "pt": "O contexto é um fator primordial para o desempenho do LLM. Pesquisas extensivas com usuários mostram que um contexto específico ajuda o LLM a identificar as leis, fatos e análises corretas a serem aplicadas. Quando o LLM tem acesso à legislação e fatos relevantes, o modelo fundamenta sua análise no quadro jurídico adequado e evita introduzir fatores irrelevantes. Isso leva a respostas que abordam a questão real em pauta, em vez de recorrer a declarações genéricas sobre a lei. Fornecer contexto geográfico (por exemplo, jurisdição) é particularmente importante, pois as leis variam significativamente entre estados e países. Mesmo que os LLMs conheçam a lei em teoria, eles tendem a recorrer a interpretações gerais sem um contexto específico.",
    }
    technique2_example_question = {
        "en": "Is an oral contract enforceable?",
        "pt": "Um contrato verbal é válido?",
    }
    technique2_example_bad_prompt = {
        "en": "Is an oral contract binding, or does it need to be in writing?",
        "pt": "Um contrato verbal é válido, ou precisa ser por escrito?",
    }
    technique2_example_good_prompt = {
        "en": "I'm a real estate investor in Florida. I verbally agreed to purchase a commercial property for $750,000, and we shook hands to seal the deal. However, we never signed any written contract. The seller now wants to back out because they received a higher offer. Given Florida's Statute of Frauds and relevant contract law, is this oral agreement legally enforceable for a real estate purchase of this value? What specific elements would I need to prove to potentially enforce this agreement, and what exceptions to the writing requirement might apply in this scenario?",
        "pt": "Sou um investidor imobiliário em São Paulo. Concordei verbalmente em comprar um imóvel comercial por R$ 750.000, e apertamos as mãos para fechar o negócio. No entanto, nunca assinamos nenhum contrato escrito. O vendedor agora quer desistir porque recebeu uma oferta maior. Considerando o artigo 108 do Código Civil brasileiro e a legislação contratual relevante, este acordo verbal é legalmente exigível para uma compra imobiliária deste valor? Quais elementos específicos eu precisaria provar para potencialmente fazer valer este acordo, e quais exceções ao requisito de escritura pública poderiam se aplicar neste cenário?",
    }
    technique2_example_explanation = {
        "en": "In the improved prompt, the context of Florida and real estate law immediately frames the question within a specific legal jurisdiction, triggering the model to apply the appropriate statutory framework (Florida's Statute of Frauds). The follow-up question asks for \"specific elements\" and \"exceptions,\" directing the model to provide a comprehensive analysis rather than a simple yes/no answer. The context also makes clear that the question concerns enforceability in a specific scenario (a $750,000 commercial property sale) rather than oral contracts generally. This rich context guides the model to analyze whether any exceptions to the writing requirement might apply to this particular transaction, resulting in legally precise advice.",
        "pt": "No prompt aprimorado, o contexto de São Paulo e da lei imobiliária brasileira imediatamente enquadra a questão dentro de uma jurisdição legal específica, levando o modelo a aplicar o quadro estatutário apropriado (artigo 108 do Código Civil). A pergunta de acompanhamento solicita \"elementos específicos\" e \"exceções\", direcionando o modelo a fornecer uma análise abrangente em vez de uma simples resposta sim/não. O contexto também deixa claro que a questão diz respeito à exigibilidade em um cenário específico (uma venda de imóvel comercial de R$ 750.000) e não a contratos verbais em geral. Este contexto rico orienta o modelo a analisar se quaisquer exceções ao requisito de escritura pública podem se aplicar a esta transação específica, resultando em um aconselhamento juridicamente preciso.",
    }
    technique2_resource_title = {
        "en": "LLMs Can Generate Rich Context from Scratch",
        "pt": "LLMs Podem Gerar Contexto Rico do Zero",
    }
    technique2_resource_url = 'https://arxiv.org/abs/2307.07169'
    technique2_resource_description = {
        "en": "Research paper showing how context helps LLMs generate better results",
        "pt": "Artigo de pesquisa mostrando como o contexto ajuda os LLMs a gerar melhores resultados",
    }
    return


@app.cell
def _():
    # Cell: Define Technique 3
    technique3_slug = 'constraint-based'
    technique3_name = {
        "en": "Constraint-Based Prompting (Conditional and Focused Instructions)",
        "pt": "Prompting Baseado em Restrições (Instruções Condicionais e Focadas)",
    }
    technique3_description = {
        "en": "Constraint-based prompting introduces explicit conditions or limits into your prompt to narrow the scope of the AI's response. This can take the form of conditional instructions (e.g., \"If X is true, do Y; if not, say it's not applicable.\") or other constraints like word limits, format requirements, or focusing on a specific subsection of content. The goal is to have the LLM only address a particular area or follow certain rules, rather than responding broadly. For example, when analyzing a lengthy contract, you might write: \"If the contract contains a termination clause, summarize that clause. Ignore other provisions.\" Similarly, you can constrain output length (\"in 100 words\") or style (\"list 3 key points\"). By setting clear boundaries or prerequisites in the prompt, you guide the model to produce a more targeted answer.",
        "pt": "O prompting baseado em restrições introduz condições ou limites explícitos em seu prompt para restringir o escopo da resposta da IA. Isso pode assumir a forma de instruções condicionais (por exemplo, \"Se X for verdadeiro, faça Y; caso contrário, diga que não é aplicável.\") ou outras restrições como limites de palavras, requisitos de formato ou foco em uma subseção específica do conteúdo. O objetivo é fazer com que o LLM aborde apenas uma área específica ou siga certas regras, em vez de responder amplamente. Por exemplo, ao analisar um contrato longo, você pode escrever: \"Se o contrato contiver uma cláusula de rescisão, resuma essa cláusula. Ignore outras disposições.\" Da mesma forma, você pode restringir o comprimento da saída (\"em 100 palavras\") ou o estilo (\"liste 3 pontos-chave\"). Ao definir limites claros ou pré-requisitos no prompt, você orienta o modelo a produzir uma resposta mais direcionada.",
    }
    technique3_why_it_works = {
        "en": "Constraints help narrow down the AI's focus so it doesn't stray into irrelevant territory. Large language models will try to use everything in the prompt to generate an answer, so if you tell it exactly what not to do or what specific subset to concentrate on, you reduce noise and off-point results. Legal professionals often only need certain information (for instance, just the holding of a case, or just one contract clause) — constraints ensure the AI filters its output to those needs. Authoritative sources recommend setting conditions or scope in prompts to make the analysis \"contextually appropriate and relevant to your needs,\" thereby cutting out unnecessary results. Additionally, adding constraints like length or format limits can improve clarity; it forces the model to be concise and stick to the requested structure. In essence, constraint-based prompting is about precision: it directs the LLM to comply with specific requirements, much like a lawyer telling a junior associate, \"Give me only the relevant facts on X and nothing else.\"",
        "pt": "Restrições ajudam a restringir o foco da IA para que ela não se desvie para território irrelevante. Modelos de linguagem grandes tentarão usar tudo no prompt para gerar uma resposta, então se você disser exatamente o que não fazer ou em qual subconjunto específico se concentrar, você reduz o ruído e os resultados fora do ponto. Profissionais jurídicos muitas vezes precisam apenas de certas informações (por exemplo, apenas a decisão de um caso, ou apenas uma cláusula contratual) — restrições garantem que a IA filtre sua saída para essas necessidades. Fontes autoritativas recomendam definir condições ou escopo nos prompts para tornar a análise \"contextualmente apropriada e relevante para suas necessidades\", eliminando assim resultados desnecessários. Além disso, adicionar restrições como limites de comprimento ou formato pode melhorar a clareza; força o modelo a ser conciso e a aderir à estrutura solicitada. Em essência, o prompting baseado em restrições é sobre precisão: direciona o LLM a cumprir requisitos específicos, muito como um advogado dizendo a um associado júnior: \"Dê-me apenas os fatos relevantes sobre X e nada mais.\"",
    }
    technique3_example_question = {
        "en": "Summarizing a specific part of a contract. (The user has a long employment contract but only cares about termination terms.)",
        "pt": "Resumindo uma parte específica de um contrato. (O usuário tem um longo contrato de trabalho, mas só se importa com os termos de rescisão.)",
    }
    technique3_example_bad_prompt = {
        "en": "Summarize this employment contract.",
        "pt": "Resuma este contrato de trabalho.",
    }
    technique3_example_good_prompt = {
        "en": "If the following employment contract contains a Termination or Severance clause, summarize those provisions in detail, focusing only on termination conditions and any severance pay terms. If not, respond that the contract has no such provisions. Ignore other sections.",
        "pt": "Se o seguinte contrato de trabalho contiver uma cláusula de Rescisão ou Indenização, resuma essas disposições em detalhes, focando apenas nas condições de rescisão e quaisquer termos de pagamento de indenização. Caso contrário, responda que o contrato não possui tais disposições. Ignore outras seções.",
    }
    technique3_example_explanation = {
        "en": "The prompt explicitly sets a condition and scope: it tells the AI to look for termination or severance clauses and report on those and nothing else. It also provides a conditional fallback (\\\"if not, say there are none\\\") so the AI won't wander off-topic if the condition isn't met. This focused instruction ensures the AI's output will directly address the user's need (termination terms) without extraneous contract details. It also implicitly instructs the AI to read the contract text (provided in the prompt) with an eye only for a specific subject, which is akin to running a targeted search within the text.\\n\\nExample output: \\\"Termination Clause (Section 5): The contract allows either party to terminate with 30 days' written notice. However, if the employee is terminated for cause (defined as gross misconduct or violation of company policy), the employer can terminate immediately without notice. The clause specifies that termination must be communicated in writing and outlines a post-termination non-compete period of 6 months.\\n\\nSeverance Provision (Section 6): In cases of termination without cause, the employee is entitled to a severance payment equal to 3 months' salary. The severance is conditioned on the employee signing a release of claims. No severance is given if the termination is for cause or if the employee resigns.\\\"",
        "pt": "O prompt define explicitamente uma condição e escopo: diz à IA para procurar cláusulas de rescisão ou indenização e relatar sobre elas e nada mais. Ele também fornece um fallback condicional (\\\"caso contrário, diga que não há nenhuma\\\") para que a IA não se desvie do tópico se a condição não for atendida. Esta instrução focada garante que a saída da IA abordará diretamente a necessidade do usuário (termos de rescisão) sem detalhes contratuais estranhos. Também instrui implicitamente a IA a ler o texto do contrato (fornecido no prompt) com atenção apenas para um assunto específico, o que é semelhante a executar uma pesquisa direcionada dentro do texto.\\\\n\\\\nExemplo de saída: \\\"Cláusula de Rescisão (Seção 5): O contrato permite que qualquer uma das partes rescinda com 30 dias de aviso prévio por escrito. No entanto, se o funcionário for demitido por justa causa (definida como má conduta grave ou violação da política da empresa), o empregador pode rescindir imediatamente sem aviso prévio. A cláusula especifica que a rescisão deve ser comunicada por escrito e descreve um período de não concorrência pós-rescisão de 6 meses.\\\\n\\\\nDisposição de Indenização (Seção 6): Em casos de rescisão sem justa causa, o funcionário tem direito a um pagamento de indenização igual a 3 meses de salário. A indenização está condicionada à assinatura de um termo de quitação pelo funcionário. Nenhuma indenização é dada se a rescisão for por justa causa ou se o funcionário renunciar.\\\"",
    }
    technique3_resource_title = {
        "en": "Prompt Engineering and Priming in Law",
        "pt": "Engenharia de Prompt e Priming em Direito",
    }
    technique3_resource_url = (
        'https://www.researchgate.net/publication/382878312_Prompt_Engineering_and_Priming_in_Law'
    )
    technique3_resource_description = {
        "en": "Research on effective prompt engineering techniques for legal applications",
        "pt": "Pesquisa sobre técnicas eficazes de engenharia de prompt para aplicações jurídicas",
    }
    return


@app.cell
def _():
    # Cell: Technique 4 Definition
    technique4_slug = 'example-few-shot'
    technique4_name = {
        "en": "Example (Few-Shot) Prompting (Providing Exemplars or Templates)",
        "pt": "Prompt por Exemplos (Few-Shot) (Fornecimento de Exemplares ou Modelos)",
    }
    technique4_description = {
        "en": "Example prompting, also known as few-shot prompting, involves including sample inputs/outputs or a template in your prompt to demonstrate the desired format, style, or level of detail. This can mean giving the AI one or more Q&A examples before your actual question, or providing a model answer structure. In the legal context, you might show an example of a well-written clause, then ask the AI to draft a similar clause for a new scenario. For instance: \\\"Example – Clause: 'In the event of breach, the non-breaching party shall… [legal language] …' Now draft a liability waiver clause for a service contract in a similar style.\\\" Another use is to provide a few sample legal questions with correct answers (few-shot Q&A) before posing a new question, which primes the model on the approach. By doing so, you leverage the AI's pattern recognition strength: it will mimic the structure or reasoning of the examples when generating the new answer.",
        "pt": "O prompt por exemplos, também conhecido como prompt few-shot, envolve incluir exemplos de entradas/saídas ou um modelo em seu prompt para demonstrar o formato, estilo ou nível de detalhe desejado. Isso pode significar dar à IA um ou mais exemplos de P&R antes de sua pergunta real, ou fornecer uma estrutura de resposta modelo. No contexto jurídico, você pode mostrar um exemplo de uma cláusula bem escrita e, em seguida, pedir à IA para redigir uma cláusula semelhante para um novo cenário. Por exemplo: \\\"Exemplo – Cláusula: \\\\\\'Em caso de violação, a parte não infratora deverá… [linguagem jurídica] …\\\\\\\' Agora redija uma cláusula de isenção de responsabilidade para um contrato de serviço em estilo semelhante.\\\" Outro uso é fornecer algumas perguntas legais de exemplo com respostas corretas (P&R few-shot) antes de fazer uma nova pergunta, o que prepara o modelo na abordagem. Ao fazer isso, você aproveita a força de reconhecimento de padrões da IA: ela imitará a estrutura ou o raciocínio dos exemplos ao gerar a nova resposta.",
    }
    technique4_why_it_works = {
        "en": "Large language models learn and operate by recognizing patterns. When you provide a sample of a good response, you essentially program the model with a mini example of the task at hand. The model will infer the style, tone, and logic from the example and apply it to the new prompt. This few-shot prompting technique is well-documented to improve performance, especially for niche tasks or formats that the model might not guess on its own. Instead of relying on the AI to deduce the desired output style, you show it explicitly. Authoritative guidelines for legal AI suggest offering a template or bullet-point structure to guide the AI's response. For example, telling the model, \"Follow this structure: 1) Facts, 2) Issue, 3) Holding\" can lead to an answer in that format. Similarly, providing a placeholder-filled template (e.g., using bracketed placeholders in an example contract clause) lets the AI know exactly how to format the answer. By demonstration, we reduce ambiguity — the AI doesn't have to \"figure out\" the format or level of detail, it just continues the pattern. This results in output that is closer to the user's expected answer in both form and substance.",
        "pt": "Modelos de linguagem grandes aprendem e operam reconhecendo padrões. Quando você fornece uma amostra de uma boa resposta, você essencialmente programa o modelo com um mini exemplo da tarefa em questão. O modelo inferirá o estilo, tom e lógica do exemplo e o aplicará ao novo prompt. Esta técnica de prompt few-shot é bem documentada para melhorar o desempenho, especialmente para tarefas de nicho ou formatos que o modelo pode não adivinhar por conta própria. Em vez de confiar na IA para deduzir o estilo de saída desejado, você o mostra explicitamente. Diretrizes autoritativas para IA jurídica sugerem oferecer um modelo ou estrutura de pontos para guiar a resposta da IA. Por exemplo, dizer ao modelo: \"Siga esta estrutura: 1) Fatos, 2) Questão, 3) Decisão\" pode levar a uma resposta nesse formato. Da mesma forma, fornecer um modelo preenchido com espaços reservados (por exemplo, usando espaços reservados entre colchetes em uma cláusula de contrato de exemplo) permite que a IA saiba exatamente como formatar a resposta. Por demonstração, reduzimos a ambiguidade — a IA não precisa \"descobrir\" o formato ou o nível de detalhe, ela apenas continua o padrão. Isso resulta em uma saída mais próxima da resposta esperada pelo usuário, tanto na forma quanto na substância.",
    }
    technique4_example_question = {
        "en": "Drafting a contract clause with a specific style. (The user wants a liability waiver clause similar to an example they like.)",
        "pt": "Redigindo uma cláusula contratual com um estilo específico. (O usuário deseja uma cláusula de isenção de responsabilidade semelhante a um exemplo que ele gosta.)",
    }
    technique4_example_bad_prompt = {
        "en": "\"Draft a liability waiver clause for a service contract.\"",
        "pt": "\"Redija uma cláusula de isenção de responsabilidade para um contrato de serviço.\"",
    }
    technique4_example_good_prompt = {
        "en": "\"Draft a liability waiver clause for a service contract. Use the following clause as a style guide and follow a similar structure and tone:\\n\\nExample Clause: \\\"In no event shall [Party] be liable for any indirect, incidental, or consequential damages arising out of or related to this Agreement, except in cases of gross negligence or willful misconduct…\\\"\\n\\nNow, write the liability waiver for our contract in a similar style, adjusting details for our context (a software service provider).\"",
        "pt": "\"Redija uma cláusula de isenção de responsabilidade para um contrato de serviço. Use a seguinte cláusula como guia de estilo e siga uma estrutura e tom semelhantes:\\\\n\\\\nCláusula Exemplo: \\\"Em nenhuma hipótese [Parte] será responsável por quaisquer danos indiretos, incidentais ou consequenciais decorrentes de ou relacionados a este Contrato, exceto em casos de negligência grave ou má conduta intencional…\\\"\\\\n\\\\nAgora, escreva a isenção de responsabilidade para nosso contrato em estilo semelhante, ajustando os detalhes para nosso contexto (um provedor de serviços de software).\"",
    }
    technique4_example_explanation = {
        "en": "The good prompt provides a concrete example clause that demonstrates the desired style (it's concise, includes a standard exclusion of indirect damages, and has an exception for gross negligence). By instructing the AI to use it as a guide, the model will mirror that phrasing and structure when drafting the new clause. The prompt also specifies the context (software service provider) so the AI can adjust any particulars (for instance, referencing \"software or data\" in the waiver if relevant). This approach reduces the guesswork for the AI – it knows exactly the kind of clause the user wants, resulting in a clause that likely aligns with industry standards or the user's preference as shown in the example.\\n\\nExample output: \\\"Liability Waiver Clause: In no event shall either party be liable to the other for any indirect, special, incidental, or consequential damages (including lost profits or data loss) arising out of or related to this Agreement or the services provided, even if such party has been advised of the possibility of such damages. The foregoing limitation applies to all causes of action, whether arising in contract, tort, or otherwise, except that nothing in this Agreement shall limit or exclude liability for a party's gross negligence or willful misconduct.\\\"\\n\\nThe output clause closely follows the style of the example: it uses the \\\"In no event shall…\\\" phrasing, disclaims indirect damages, and includes an exception for gross negligence/willful misconduct. By contrast, a clause generated without the example might have been structured differently or missed including the exception. The example prompt ensured the result was aligned with the desired template.",
        "pt": "O bom prompt fornece uma cláusula de exemplo concreta que demonstra o estilo desejado (é concisa, inclui uma exclusão padrão de danos indiretos e tem uma exceção para negligência grave). Ao instruir a IA a usá-la como guia, o modelo espelhará essa fraseologia e estrutura ao redigir a nova cláusula. O prompt também especifica o contexto (provedor de serviços de software) para que a IA possa ajustar quaisquer particularidades (por exemplo, referenciando \"software ou dados\" na isenção, se relevante). Essa abordagem reduz a adivinhação para a IA – ela sabe exatamente o tipo de cláusula que o usuário deseja, resultando em uma cláusula que provavelmente se alinha aos padrões da indústria ou à preferência do usuário, como mostrado no exemplo.\\\\n\\\\nExemplo de saída: \\\"Cláusula de Isenção de Responsabilidade: Em nenhuma hipótese qualquer das partes será responsável perante a outra por quaisquer danos indiretos, especiais, incidentais ou consequenciais (incluindo lucros cessantes ou perda de dados) decorrentes de ou relacionados a este Contrato ou aos serviços prestados, mesmo que tal parte tenha sido avisada da possibilidade de tais danos. A limitação precedente aplica-se a todas as causas de pedir, quer surjam em contrato, ato ilícito ou de outra forma, exceto que nada neste Contrato limitará ou excluirá a responsabilidade por negligência grave ou má conduta intencional de uma parte.\\\"\\\\n\\\\nA cláusula de saída segue de perto o estilo do exemplo: usa a fraseologia \\\"Em nenhuma hipótese…\\\", isenta danos indiretos e inclui uma exceção para negligência grave/má conduta intencional. Em contraste, uma cláusula gerada sem o exemplo poderia ter sido estruturada de forma diferente ou ter deixado de incluir a exceção. O prompt de exemplo garantiu que o resultado estivesse alinhado com o modelo desejado.",
    }
    technique4_resource_title = {
        "en": "Minnesota Law Review Article on LLMs in Legal Practice",
        "pt": "Artigo da Minnesota Law Review sobre LLMs na Prática Jurídica",
    }
    technique4_resource_url = (
        'https://minnesotalawreview.org/wp-content/uploads/2023/10/FL1-Choi-Schwarcz.pdf'
    )
    technique4_resource_description = {
        "en": "Comprehensive exploration of few-shot prompting techniques in legal contexts",
        "pt": "Exploração abrangente de técnicas de prompt few-shot em contextos jurídicos",
    }
    return


@app.cell
def _():
    technique5_slug = 'step-by-step'
    technique5_name = {
        "en": "Step-by-Step Prompting (Chain-of-Thought Legal Reasoning)",
        "pt": "Prompting Passo a Passo (Raciocínio Jurídico em Cadeia de Pensamento)",
    }
    technique5_description = {
        "en": "Step-by-step prompting involves asking the LLM to work through the problem in a logical sequence, rather than jumping straight to a conclusion. In legal tasks, this often means prompting the model to apply a structured analysis (for example, the IRAC method: Issue, Rule, Application, Conclusion, or breaking down elements of a legal test). You can achieve this by explicitly instructing the AI how to structure its reasoning. For instance: \"Analyze this scenario step by step: first identify the legal issues, then state the relevant law for each issue, apply the facts, and finally give a conclusion.\" or simply \"Let's think this through step-by-step.\". Another variant is telling the model to enumerate its reasoning (e.g., \"1, 2, 3…\"). The idea is to mimic how a lawyer would deliberate on a problem methodically. This technique is especially useful for complex scenarios with multiple factors (such as determining if negligence is present, which requires analyzing duty, breach, causation, damages in turn).",
        "pt": "O prompting passo a passo envolve pedir ao LLM para trabalhar o problema em uma sequência lógica, em vez de pular direto para uma conclusão. Em tarefas jurídicas, isso geralmente significa solicitar ao modelo que aplique uma análise estruturada (por exemplo, o método IRAC: Questão, Regra, Aplicação, Conclusão, ou decompor elementos de um teste legal). Você pode conseguir isso instruindo explicitamente a IA sobre como estruturar seu raciocínio. Por exemplo: \"Analise este cenário passo a passo: primeiro identifique as questões legais, depois declare a lei relevante para cada questão, aplique os fatos e, finalmente, dê uma conclusão.\" ou simplesmente \"Vamos pensar nisso passo a passo.\". Outra variante é dizer ao modelo para enumerar seu raciocínio (por exemplo, \"1, 2, 3…\"). A ideia é imitar como um advogado deliberaria sobre um problema metodicamente. Esta técnica é especialmente útil para cenários complexos com múltiplos fatores (como determinar se há negligência, o que requer análise de dever, violação, causalidade, danos, sucessivamente).",
    }
    technique5_why_it_works = {
        "en": "Prompting an LLM to show its work leads to more transparent and often more accurate results. Recent findings highlight that users can significantly improve answer quality by asking the model to \"reason step by step.\" This approach, known as chain-of-thought prompting, has been widely adopted because it helps the AI break down complex tasks instead of making a leap and possibly an error. By structuring the analysis (much like IRAC or element-by-element examination), you not only get a thorough answer but can also verify each step of the reasoning. If the model makes a mistake in a step, you can catch it and correct it, resulting in a more reliable final answer. In legal reasoning, where analytical rigor is key, this method ensures the AI considers all necessary components (for example, each element of a claim or each prong of a test). It effectively guides the model to \"think like a lawyer,\" aligning its process with how a legal professional would logically approach the issue. Even if newer LLMs can sometimes do this internally, explicitly prompting for step-by-step reasoning is a safe way to enforce completeness and clarity in the output.",
        "pt": "Solicitar a um LLM que mostre seu trabalho leva a resultados mais transparentes e muitas vezes mais precisos. Descobertas recentes destacam que os usuários podem melhorar significativamente a qualidade da resposta pedindo ao modelo para \"raciocinar passo a passo\". Essa abordagem, conhecida como prompting em cadeia de pensamento, foi amplamente adotada porque ajuda a IA a decompor tarefas complexas em vez de dar um salto e possivelmente cometer um erro. Ao estruturar a análise (muito como IRAC ou exame elemento por elemento), você não apenas obtém uma resposta completa, mas também pode verificar cada etapa do raciocínio. Se o modelo cometer um erro em uma etapa, você pode detectá-lo e corrigi-lo, resultando em uma resposta final mais confiável. No raciocínio jurídico, onde o rigor analítico é fundamental, este método garante que a IA considere todos os componentes necessários (por exemplo, cada elemento de uma reivindicação ou cada parte de um teste). Ele efetivamente guia o modelo a \"pensar como um advogado\", alinhando seu processo com a forma como um profissional jurídico abordaria logicamente a questão. Mesmo que LLMs mais recentes possam às vezes fazer isso internamente, solicitar explicitamente o raciocínio passo a passo é uma maneira segura de impor completude e clareza na saída.",
    }
    technique5_example_question = {
        "en": "Assessing legal liability with multiple elements. (A customer slipped and fell in a store – does the store have negligence liability?)",
        "pt": "Avaliando a responsabilidade legal com múltiplos elementos. (Um cliente escorregou e caiu em uma loja – a loja tem responsabilidade por negligência?)",
    }
    technique5_example_bad_prompt = {
        "en": "The customer slipped on a wet floor in the store and was injured. Is the store liable for negligence?",
        "pt": "O cliente escorregou em um piso molhado na loja e se machucou. A loja é responsável por negligência?",
    }
    technique5_example_good_prompt = {
        "en": "You are a legal analyst. Analyze the following scenario step by step to determine if the store could be held liable for negligence: A customer in a grocery store slipped on a spilled liquid and broke their arm. First, identify the elements required to prove negligence in U.S. law (duty, breach, causation, damages). Then, discuss each element one by one with respect to the facts (e.g., did the store owe a duty, did it breach that duty by not cleaning the spill, etc.). Conclude whether the elements are satisfied and thus if the store is likely liable.",
        "pt": "Você é um analista jurídico. Analise o seguinte cenário passo a passo para determinar se a loja pode ser responsabilizada por negligência: Um cliente em um supermercado escorregou em um líquido derramado e quebrou o braço. Primeiro, identifique os elementos necessários para provar negligência na lei brasileira (conduta culposa, dano, nexo causal). Em seguida, discuta cada elemento um por um com relação aos fatos (por exemplo, a loja tinha um dever de cuidado, violou esse dever ao não limpar o derramamento, etc.). Conclua se os elementos estão satisfeitos e, portanto, se a loja é provavelmente responsável.",
    }
    technique5_example_explanation = {
        "en": "This prompt explicitly asks for a step-by-step IRAC-style analysis. It not only tells the AI to consider each negligence element in order but also reminds it of what those elements are. The instruction ensures the answer will be organized (perhaps with headings or paragraphs for Duty, Breach, Causation, Damages, Conclusion). The model is less likely to omit a part of the analysis, and the user will get a structured explanation rather than a one-liner. By guiding the reasoning process, the prompt helps the AI reach a well-founded conclusion (or identify if information is missing) just as a human lawyer would.\\n\\nExample output: \\\"*Duty: The store, as a business open to the public, owes its customers a legal duty of care to maintain the premises in a reasonably safe condition. Here, that duty means regularly inspecting for hazards like spills and either cleaning them promptly or warning customers (e.g., with a 'Wet Floor' sign).\\n\\nBreach: We examine if the store breached its duty by failing to address the spilled liquid. If the spill was present long enough that employees should have noticed it (say, it had been on the floor for 30 minutes without cleanup), not cleaning it would likely be a breach of duty. If the spill happened moments before the fall, the store might argue it had no reasonable opportunity to discover and fix it, which could negate breach.\\n\\nCausation: The customer's injury must be caused by the store's breach. Here, the causal link is direct: the unsafe condition (wet floor) led to the slip-and-fall accident. We'd also consider proximate cause – it's foreseeable that an unaddressed spill leads to this kind of injury, so causation is established.\\n\\nDamages: The customer suffered actual harm (a broken arm, medical bills, etc.), satisfying the damages element required for negligence.\\n\\nConclusion: If evidence shows the spill was on the floor long enough that the store should have known and cleaned it, the store likely breached its duty. In that case, all four elements of negligence are met, and the store would likely be held liable for the customer's injury. If the spill was truly sudden and unforeseeable, the store might avoid liability, but absent such proof, this scenario points toward negligence on the store's part.*\\\"",
        "pt": "Este prompt solicita explicitamente uma análise passo a passo no estilo IRAC. Ele não apenas diz à IA para considerar cada elemento de negligência em ordem, mas também a lembra quais são esses elementos. A instrução garante que a resposta será organizada (talvez com títulos ou parágrafos para Dever, Violação, Causalidade, Danos, Conclusão). O modelo tem menos probabilidade de omitir uma parte da análise, e o usuário obterá uma explicação estruturada em vez de uma resposta de uma linha. Ao guiar o processo de raciocínio, o prompt ajuda a IA a chegar a uma conclusão bem fundamentada (ou identificar se falta informação) assim como um advogado humano faria.\\\\n\\\\nExemplo de saída: \\\"*Dever: A loja, como um negócio aberto ao público, deve aos seus clientes um dever legal de cuidado para manter as instalações em condições razoavelmente seguras. Aqui, esse dever significa inspecionar regularmente por perigos como derramamentos e limpá-los prontamente ou avisar os clientes (por exemplo, com uma placa de \\\\\\'Piso Molhado\\\\\\').\\\\n\\\\nViolação: Examinamos se a loja violou seu dever ao não lidar com o líquido derramado. Se o derramamento esteve presente por tempo suficiente para que os funcionários devessem tê-lo notado (digamos, estava no chão por 30 minutos sem limpeza), não limpá-lo provavelmente seria uma violação do dever. Se o derramamento aconteceu momentos antes da queda, a loja poderia argumentar que não teve oportunidade razoável de descobri-lo e corrigi-lo, o que poderia negar a violação.\\\\n\\\\nCausalidade: A lesão do cliente deve ser causada pela violação da loja. Aqui, o nexo causal é direto: a condição insegura (piso molhado) levou ao acidente de escorregão e queda. Também consideraríamos a causa próxima – é previsível que um derramamento não tratado leve a esse tipo de lesão, então a causalidade está estabelecida.\\\\n\\\\nDanos: O cliente sofreu dano real (um braço quebrado, contas médicas, etc.), satisfazendo o elemento de danos necessário para negligência.\\\\n\\\\nConclusão: Se as evidências mostrarem que o derramamento estava no chão por tempo suficiente para que a loja devesse saber e limpá-lo, a loja provavelmente violou seu dever. Nesse caso, todos os quatro elementos de negligência são atendidos, e a loja provavelmente seria responsabilizada pela lesão do cliente. Se o derramamento foi verdadeiramente súbito e imprevisível, a loja poderia evitar a responsabilidade, mas na ausência de tal prova, este cenário aponta para negligência por parte da loja.*\\\"",
    }
    technique5_resource_title = {
        "en": "Deloitte's Guide to Legal Prompting",
        "pt": "Guia da Deloitte para Prompting Jurídico",
    }
    technique5_resource_url = (
        'https://www2.deloitte.com/dl/en/pages/legal/articles/grundkurs-legal-prompting.html'
    )
    technique5_resource_description = {
        "en": "Comprehensive guide on effective legal prompting techniques including step-by-step reasoning",
        "pt": "Guia abrangente sobre técnicas eficazes de prompting jurídico, incluindo raciocínio passo a passo",
    }
    return


@app.cell
def _():
    technique6_slug = 'contract-extraction'
    technique6_name = {
        "en": "Extracting Key Provisions and Data from Contracts",
        "pt": "Extraindo Disposições e Dados Chave de Contratos",
    }
    technique6_description = {
        "en": "This technique involves directing an LLM to locate and extract specific information from legal documents like contracts, rather than summarizing the entire document. By focusing the model on particular provisions, clauses, or data points, attorneys can quickly find relevant information such as dates, obligations, defined terms, or conditions. The approach is similar to using targeted questions with a colleague who has read a document - except the LLM does the quick read-through and extraction for you.",
        "pt": "Esta técnica envolve direcionar um LLM para localizar e extrair informações específicas de documentos legais como contratos, em vez de resumir o documento inteiro. Ao focar o modelo em disposições, cláusulas ou pontos de dados específicos, os advogados podem encontrar rapidamente informações relevantes como datas, obrigações, termos definidos ou condições. A abordagem é semelhante a usar perguntas direcionadas com um colega que leu um documento - exceto que o LLM faz a leitura rápida e a extração para você.",
    }
    technique6_why_it_works = {
        "en": "Legal documents are often lengthy and complex, with critical details buried within dense paragraphs. By prompting the LLM to focus on specific provisions or information types, you eliminate the noise and zero in on what matters. This technique works because LLMs have strong pattern recognition abilities that can identify the relevant clauses or data points when properly directed. Rather than processing the entire document (which might exceed the model's context window anyway), a targeted extraction prompt creates efficiency by pulling only the needed information. This is particularly valuable when reviewing multiple agreements or when specific contractual elements (like termination rights, payment terms, or warranty provisions) need quick assessment across documents.",
        "pt": "Documentos legais são frequentemente longos e complexos, com detalhes críticos enterrados em parágrafos densos. Ao solicitar ao LLM que se concentre em disposições ou tipos de informação específicos, você elimina o ruído e foca no que importa. Esta técnica funciona porque os LLMs têm fortes habilidades de reconhecimento de padrões que podem identificar as cláusulas ou pontos de dados relevantes quando devidamente direcionados. Em vez de processar o documento inteiro (o que pode exceder a janela de contexto do modelo de qualquer maneira), um prompt de extração direcionado cria eficiência ao puxar apenas as informações necessárias. Isso é particularmente valioso ao revisar múltiplos acordos ou quando elementos contratuais específicos (como direitos de rescisão, termos de pagamento ou disposições de garantia) precisam de avaliação rápida entre documentos.",
    }
    technique6_example_question = {
        "en": "Understanding a contract's liquidated damages provision. (You need to know how damages for breach are handled in a long agreement.)",
        "pt": "Entendendo a cláusula de liquidação de danos de um contrato. (Você precisa saber como os danos por violação são tratados em um longo acordo.)",
    }
    technique6_example_bad_prompt = {
        "en": "Tell me about this contract. [entire 50-page contract pasted]",
        "pt": "Fale-me sobre este contrato. [contrato inteiro de 50 páginas colado]",
    }
    technique6_example_good_prompt = {
        "en": "In the clause below, what do the parties agree regarding damages for breach?\\n\\n12.2 Liquidated Damages Not Penalty. Because of the unique nature of the economic damages that may be sustained by the Company in the event of a breach of certain provisions of this Agreement by Executive, it is acknowledged and agreed by the Parties that it would be impracticable and extremely difficult to ascertain with any degree of certainty the amount of damages which the Company would sustain as a result of such breach. Accordingly, if Executive breaches certain provisions of this Agreement, the Parties agree that any sums payable under this Agreement in such circumstances are in the nature of liquidated damages and not a penalty, and represent a reasonable estimate of the damages that the Company will suffer in the event of Executive's breach.\\n\\nSummarize the effect of this clause in bullet points, explaining what this means for both parties if there's a breach.",
        "pt": "Na cláusula abaixo, o que as partes concordam sobre danos por violação?\\\\n\\\\n12.2 Danos Liquidados Não Penalidade. Devido à natureza única dos danos econômicos que podem ser sofridos pela Empresa no caso de violação de certas disposições deste Contrato pelo Executivo, é reconhecido e acordado pelas Partes que seria impraticável e extremamente difícil determinar com qualquer grau de certeza o montante dos danos que a Empresa sofreria como resultado de tal violação. Assim, se o Executivo violar certas disposições deste Contrato, as Partes concordam que quaisquer somas pagáveis sob este Contrato em tais circunstâncias são de natureza de danos liquidados e não uma penalidade, e representam uma estimativa razoável dos danos que a Empresa sofrerá no caso de violação do Executivo.\\\\n\\\\nResuma o efeito desta cláusula em pontos, explicando o que isso significa para ambas as partes se houver uma violação.",
    }
    technique6_example_explanation = {
        "en": "The good prompt does several things right: it isolates just the relevant clause (12.2) rather than sending the entire contract, asks a specific question about breach damages, and requests a structured response format (bullet points). This leads the LLM to focus solely on interpreting the liquidated damages provision, which establishes that certain payments for breach: 1) are considered liquidated damages not penalties, 2) are justified because actual damages would be difficult to measure, and 3) represent what the parties agree is a reasonable estimate of potential harm. The model doesn't waste time analyzing unrelated sections of the agreement, and the attorney gets precisely the information needed: the nature and justification of the damages provision. This extraction approach is significantly more efficient than asking for a general contract summary and then hunting through it for damage provisions.\\n\\nExample output: \\\"• Effect of Clause 12.2 - Liquidated Damages:\\n• The clause establishes that certain breach payments are classified as liquidated damages, not penalties\\n• Both parties acknowledge that actual economic damages from specific breaches would be difficult to calculate with certainty\\n• The payments represent a reasonable pre-estimate of potential damages, not punishment\\n• This classification matters legally because courts generally enforce liquidated damages provisions but may invalidate penalty clauses\\n• For the executive: limits potential argument that the damages are excessive or punitive\\n• For the company: provides more certainty that the damage amounts will be enforceable if challenged in court\\\"",
        "pt": "O bom prompt faz várias coisas certas: isola apenas a cláusula relevante (12.2) em vez de enviar o contrato inteiro, faz uma pergunta específica sobre danos por violação e solicita um formato de resposta estruturado (pontos). Isso leva o LLM a focar exclusivamente na interpretação da disposição de danos liquidados, que estabelece que certos pagamentos por violação: 1) são considerados danos liquidados, não penalidades, 2) são justificados porque os danos reais seriam difíceis de medir, e 3) representam o que as partes concordam ser uma estimativa razoável do dano potencial. O modelo não perde tempo analisando seções não relacionadas do acordo, e o advogado obtém precisamente a informação necessária: a natureza e a justificação da disposição sobre danos. Esta abordagem de extração é significativamente mais eficiente do que pedir um resumo geral do contrato e depois procurar nele por disposições sobre danos.\\\\n\\\\nExemplo de saída: \\\"• Efeito da Cláusula 12.2 - Danos Liquidados:\\\\n• A cláusula estabelece que certos pagamentos por violação são classificados como danos liquidados, não penalidades\\\\n• Ambas as partes reconhecem que os danos econômicos reais de violações específicas seriam difíceis de calcular com certeza\\\\n• Os pagamentos representam uma estimativa prévia razoável de danos potenciais, não punição\\\\n• Esta classificação importa legalmente porque os tribunais geralmente aplicam disposições de danos liquidados, mas podem invalidar cláusulas penais\\\\n• Para o executivo: limita o argumento potencial de que os danos são excessivos ou punitivos\\\\n• Para a empresa: fornece mais certeza de que os montantes dos danos serão aplicáveis se contestados em tribunal\\\"",
    }
    technique6_resource_title = {
        "en": "Ethylene Sales Agreement",
        "pt": "Contrato de Venda de Etileno",
    }
    technique6_resource_url = (
        'https://www.sec.gov/Archives/edgar/data/1604665/000119312514263367/d715499dex104.htm'
    )
    technique6_resource_description = {
        'en': 'A complex and long agreement, perfect for this example.',
        'pt': 'Um acordo complexo e longo, perfeito para este exemplo.',
    }
    return


@app.cell
def _():
    technique7_slug = 'msa-clause-drafting'
    technique7_name = {
        'en': 'Master Service Agreement Clause Drafting and Refinement',
        'pt': 'Elaboração e Refinamento de Cláusulas de Contrato Mestre de Serviços (MSA)',
    }
    technique7_description = {
        'en': 'This technique involves using LLMs to draft new clauses or refine existing language in Master Service Agreements (MSAs). By setting clear parameters about the purpose, required terms, governing law, and desired style, you can generate high-quality legal text that meets your specific needs. The model can either create clauses from scratch or suggest improvements to existing language, accelerating the drafting process while ensuring the output aligns with legal standards.',
        'pt': 'Esta técnica envolve o uso de LLMs para redigir novas cláusulas ou refinar a linguagem existente em Contratos Mestre de Serviços (MSAs). Ao definir parâmetros claros sobre o propósito, termos exigidos, lei aplicável e estilo desejado, você pode gerar texto legal de alta qualidade que atenda às suas necessidades específicas. O modelo pode criar cláusulas do zero ou sugerir melhorias na linguagem existente, acelerando o processo de redação enquanto garante que a saída esteja alinhada aos padrões legais.',
    }
    technique7_why_it_works = {
        'en': "LLMs have been trained on vast repositories of legal documents, including agreements filed with the SEC. This training enables them to understand the structure, terminology, and conventional language of MSAs and other legal agreements. By providing specific context (jurisdiction, industry, desired complexity level) and parameters (required elements, formatting preferences), you narrow the model's focus to produce relevant, properly structured legal text. The model can quickly generate initial drafts that follow standard legal conventions or modernize outdated language, saving significant time compared to manual drafting. However, human review remains essential to ensure the output is legally sound and contextually appropriate for your specific transaction.",
        'pt': 'LLMs foram treinados em vastos repositórios de documentos legais, incluindo acordos arquivados na SEC. Este treinamento permite que eles entendam a estrutura, terminologia e linguagem convencional de MSAs e outros acordos legais. Ao fornecer contexto específico (jurisdição, indústria, nível de complexidade desejado) e parâmetros (elementos exigidos, preferências de formatação), você restringe o foco do modelo para produzir texto legal relevante e devidamente estruturado. O modelo pode gerar rapidamente rascunhos iniciais que seguem as convenções legais padrão ou modernizar linguagem desatualizada, economizando tempo significativo em comparação com a redação manual. No entanto, a revisão humana permanece essencial para garantir que a saída seja juridicamente sólida e contextualmente apropriada para sua transação específica.',
    }
    technique7_example_question = {
        'en': 'Drafting or refining confidentiality clauses in a Master Service Agreement. (You need to create or improve language around confidential information protection.)',
        'pt': 'Redigindo ou refinando cláusulas de confidencialidade em um Contrato Mestre de Serviços. (Você precisa criar ou melhorar a linguagem sobre proteção de informações confidenciais.)',
    }
    technique7_example_bad_prompt = {
        'en': 'Write a confidentiality clause for my MSA.',
        'pt': 'Escreva uma cláusula de confidencialidade para meu MSA.',
    }
    technique7_example_good_prompt = {
        'en': 'You are a lawyer drafting a confidentiality clause for a Master Service Agreement between a technology vendor and healthcare client under California law. Reference the structure in the SEC filing at https://www.sec.gov/Archives/edgar/data/1042134/000119312505162630/dex1033.htm. The clause should cover: (1) definition of confidential information, (2) obligations to maintain secrecy, (3) standard exceptions (public information, independently developed information, etc.), (4) duration of obligations (3 years post-termination), and (5) return of confidential information upon termination. Write the clause in plain English while maintaining necessary legal protections. Format with numbered subsections for readability.',
        'pt': 'Você é um advogado redigindo uma cláusula de confidencialidade para um Contrato Mestre de Serviços entre um fornecedor de tecnologia e um cliente da área de saúde sob a lei da Califórnia. Consulte a estrutura no arquivamento da SEC em https://www.sec.gov/Archives/edgar/data/1042134/000119312505162630/dex1033.htm. A cláusula deve cobrir: (1) definição de informação confidencial, (2) obrigações de manter sigilo, (3) exceções padrão (informação pública, informação desenvolvida independentemente, etc.), (4) duração das obrigações (3 anos pós-rescisão), e (5) devolução de informação confidencial após a rescisão. Escreva a cláusula em linguagem simples, mantendo as proteções legais necessárias. Formate com subseções numeradas para legibilidade.',
    }
    technique7_example_explanation = {
        'en': "The good prompt provides extensive context and direction for creating an effective confidentiality clause. It specifies the type of agreement (MSA), the parties involved (tech vendor and healthcare client), the governing law (California), and references a specific SEC filing as a structural guide. The prompt also clearly outlines the five key elements that must be included in the clause and provides specific parameters (3-year post-termination duration). Furthermore, it guides the style ('plain English') and formatting ('numbered subsections'), ensuring the output will be both legally sound and reader-friendly.\\n\\nBy contrast, the bad prompt gives virtually no information about context, content requirements, style preferences, or formatting needs, which would likely result in a generic clause that might not address the specific needs of a technology-healthcare relationship or conform to California law. The specificity in the good prompt ensures the model produces a clause that closely matches what would appear in a professionally drafted MSA, with appropriate attention to healthcare data concerns and technology service specifics.\\n\\nThe resulting clause might begin with a definition section that carefully defines confidential information in the healthcare technology context, outline specific security measures required for protected health information, list standard exceptions to confidentiality obligations, specify the 3-year post-termination period, and detail the procedures for returning or destroying confidential information when the agreement ends.",
        'pt': "O bom prompt fornece contexto e direção extensivos para criar uma cláusula de confidencialidade eficaz. Ele especifica o tipo de acordo (MSA), as partes envolvidas (fornecedor de tecnologia e cliente da área de saúde), a lei aplicável (Califórnia) e referencia um arquivamento específico da SEC como guia estrutural. O prompt também descreve claramente os cinco elementos-chave que devem ser incluídos na cláusula e fornece parâmetros específicos (duração de 3 anos pós-rescisão). Além disso, orienta o estilo (\\'linguagem simples\\') e a formatação (\\'subseções numeradas\\'), garantindo que a saída seja juridicamente sólida e fácil de ler.\\\\n\\\\nEm contraste, o prompt ruim não fornece praticamente nenhuma informação sobre contexto, requisitos de conteúdo, preferências de estilo ou necessidades de formatação, o que provavelmente resultaria em uma cláusula genérica que poderia não atender às necessidades específicas de uma relação tecnologia-saúde ou estar em conformidade com a lei da Califórnia. A especificidade no bom prompt garante que o modelo produza uma cláusula que corresponda de perto ao que apareceria em um MSA redigido profissionalmente, com atenção apropriada às preocupações com dados de saúde e especificidades do serviço de tecnologia.\\\\n\\\\nA cláusula resultante pode começar com uma seção de definição que define cuidadosamente informações confidenciais no contexto da tecnologia da saúde, descreve medidas de segurança específicas exigidas para informações de saúde protegidas, lista exceções padrão às obrigações de confidencialidade, especifica o período pós-rescisão de 3 anos e detalha os procedimentos para devolver ou destruir informações confidenciais quando o acordo terminar.",
    }
    technique7_resource_title = {
        'en': 'Master Service Agreement',
        'pt': 'Contrato Mestre de Serviços',
    }
    technique7_resource_url = (
        'https://www.sec.gov/Archives/edgar/data/1042134/000119312505162630/dex1033.htm'
    )
    technique7_resource_description = {
        'en': 'A complex and long agreement, perfect for this example, but now techy.',
        'pt': 'Um acordo complexo e longo, perfeito para este exemplo, mas agora tecnológico.',
    }
    return


@app.cell
def _(DirectLLMClient, mo):
    # Cell 8: Display Response Function
    def display_response(user_prompt: str = None):
        """Create a nice Marimo UI element to display the prompt and response with a loading spinner."""
        if not user_prompt.value:
            return mo.md(
                """
                <div style="margin: 20px 0; border: 2px solid #9D0208; border-radius: 8px; overflow: hidden; background-color: #F9F7F4; font-family: 'Inter', sans-serif;">
                    <div style="background-color: #000000; padding: 15px; border-bottom: 2px solid #9D0208;">
                        <strong style="color: #FFFFFF; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px;">PROMPT:</strong>
                        <div style="margin-top: 8px; font-style: italic; color: #FFFFFF;">No prompt provided yet.</div>
                    </div>
                    <div style="padding: 15px;">
                        <strong style="font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px;">RESPONSE:</strong>
                        <div style="margin-top: 8px; white-space: pre-wrap;">We will have a response from the model here.</div>
                    </div>
                </div>
                """
            )

        client = DirectLLMClient(provider='openai')

        # Display a loading message with a spinner
        with mo.status.spinner(subtitle='GENERATING RESPONSE...') as spinner:
            response = client.generate(
                prompt=user_prompt.value, system_message='You are a helpful assistant.'
            )
            spinner.update(subtitle='FORMATTING RESPONSE...')

        final_response = mo.vstack(
            [
                mo.md(
                    f"""
                    <div style="margin: 20px 0; border: 2px solid #9D0208; border-radius: 8px; overflow: hidden; background-color: #F9F7F4; font-family: 'Inter', sans-serif;">
                        <div style="background-color: #000000; padding: 15px; border-bottom: 2px solid #9D0208;">
                            <strong style="color: #FFFFFF; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px;">PROMPT:</strong>
                            <div style="margin-top: 8px; font-style: italic; color: #FFFFFF;">{user_prompt.value}</div>
                        </div>
                        <div style="padding: 15px;">
                            <strong style="font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px;">RESPONSE:</strong>
                        </div>
                    </div>
                    """
                ),
                mo.md(response),
            ]
        )
        return final_response
    return (display_response,)


@app.cell
def _():
    # Cell: Define Technique 8
    technique8_slug = 'ambiguity-interpretation'
    technique8_name = {
        'en': 'Handling Ambiguity and Multiple Interpretations',
        'pt': 'Lidando com Ambiguidade e Múltiplas Interpretações',
    }
    technique8_description = {
        'en': 'Legal language is notoriously prone to ambiguity. A well-designed prompt can help explore different interpretations of a clause or identify unclear wording. If you suspect a contract clause or statute could be read in more than one way, prompt the model to analyze it from multiple angles. This technique leverages the LLM to surface different possible readings of ambiguous text, helping lawyers anticipate potential disputes or identify areas needing clearer drafting.',
        'pt': 'A linguagem jurídica é notoriamente propensa à ambiguidade. Um prompt bem elaborado pode ajudar a explorar diferentes interpretações de uma cláusula ou identificar redação pouco clara. Se você suspeitar que uma cláusula contratual ou estatuto pode ser lido de mais de uma maneira, solicite ao modelo que o analise de múltiplos ângulos. Esta técnica aproveita o LLM para trazer à tona diferentes leituras possíveis de texto ambíguo, ajudando os advogados a antecipar disputas potenciais ou identificar áreas que precisam de redação mais clara.',
    }
    technique8_why_it_works = {
        'en': 'Ambiguity in legal documents can lead to disputes and litigation. By explicitly asking an LLM to provide multiple interpretations of ambiguous language, you prevent the model from committing to a single answer and instead encourage it to explore all plausible readings. This is particularly valuable in cross-border or bilingual contracts where cultural and linguistic differences can create additional layers of ambiguity. For example, contracts between English and Chinese parties may have subtle but significant differences in translation that affect legal interpretation. The LLM can identify these potential discrepancies when properly prompted, allowing attorneys to anticipate arguments from both sides and draft clearer language. Since the model has been trained on vast legal corpora, it can recognize common patterns of ambiguity and suggest alternative readings that might not be immediately apparent, serving as a valuable thought partner in identifying potential issues before they become disputes.',
        'pt': 'A ambiguidade em documentos legais pode levar a disputas e litígios. Ao solicitar explicitamente que um LLM forneça múltiplas interpretações de linguagem ambígua, você impede que o modelo se comprometa com uma única resposta e, em vez disso, o incentiva a explorar todas as leituras plausíveis. Isso é particularmente valioso em contratos transfronteiriços ou bilíngues, onde diferenças culturais e linguísticas podem criar camadas adicionais de ambiguidade. Por exemplo, contratos entre partes inglesas e chinesas podem ter diferenças sutis, mas significativas, na tradução que afetam a interpretação legal. O LLM pode identificar essas discrepâncias potenciais quando devidamente solicitado, permitindo que os advogados antecipem argumentos de ambos os lados e redijam uma linguagem mais clara. Como o modelo foi treinado em vastos corpora legais, ele pode reconhecer padrões comuns de ambiguidade e sugerir leituras alternativas que podem não ser imediatamente aparentes, servindo como um valioso parceiro de pensamento na identificação de problemas potenciais antes que se tornem disputas.',
    }
    technique8_example_question = {
        'en': 'Analyzing a potentially ambiguous non-compete clause in a contract. (The scope of prohibited activities is unclear.)',
        'pt': 'Analisando uma cláusula de não concorrência potencialmente ambígua em um contrato. (O escopo das atividades proibidas não está claro.)',
    }
    technique8_example_bad_prompt = {
        'en': 'What does this non-compete clause mean: "Party A shall not engage in any business similar to Party B\'s business for two years in the same city"?',
        'pt': 'O que significa esta cláusula de não concorrência: "A Parte A não deve se envolver em nenhum negócio semelhante ao negócio da Parte B por dois anos na mesma cidade"?',
    }
    technique8_example_good_prompt = {
        'en': 'The following non-compete clause may be ambiguous: "Party A shall not engage in any business similar to Party B\'s business for two years in the same city." What are three different ways one could interpret the scope of "engage in any business" in this context? For each interpretation, explain: 1) What specific activities would be prohibited, 2) What activities might still be permitted, and 3) Which party would likely favor this interpretation. Then suggest a clearer rewriting that would eliminate the ambiguity.',
        'pt': 'A seguinte cláusula de não concorrência pode ser ambígua: "A Parte A não deve se envolver em nenhum negócio semelhante ao negócio da Parte B por dois anos na mesma cidade." Quais são três maneiras diferentes de interpretar o escopo de "se envolver em qualquer negócio" neste contexto? Para cada interpretação, explique: 1) Quais atividades específicas seriam proibidas, 2) Quais atividades ainda poderiam ser permitidas, e 3) Qual parte provavelmente favoreceria essa interpretação. Em seguida, sugira uma reescrita mais clara que eliminaria a ambiguidade.',
    }
    technique8_example_explanation = {
        'en': "The good prompt specifically identifies where the ambiguity lies ('engage in any business') and asks for multiple interpretations (three), with structured analysis of each. By requesting the model to explain which activities would be prohibited versus permitted under each reading, and which party would favor each interpretation, the prompt encourages a balanced, thorough analysis from different perspectives. The request for a clearer rewriting provides practical value beyond just identifying the problem. This approach transforms the LLM into a collaborative thought partner that helps anticipate potential arguments from both sides of a future dispute.\\n\\nExample output: \\\"Interpretation 1 (Broadest): 'Engage in any business' prohibits Party A from any involvement whatsoever with competing businesses, including: employment at any level, consulting work, passive investment (even minor shareholding), and of course founding or operating a competing business. Under this reading, Party A could still work in unrelated industries or in the same industry outside the specified city. Party B would favor this interpretation as it maximizes protection from competition.\\n\\nInterpretation 2 (Moderate): 'Engage in any business' means actively participating in the operation or management of a competing business, including: founding a competing company, serving as an executive or manager, or working in a significant capacity that leverages industry knowledge. Under this reading, Party A could still make passive investments or hold non-management positions in competing businesses. Neither party clearly benefits, as this represents a middle ground.\\n\\nInterpretation 3 (Narrowest): 'Engage in any business' refers only to founding, owning, or controlling a competing business. Under this reading, Party A would be prohibited from starting their own competing venture or being a controlling shareholder, but could freely work as an employee, consultant, or minor investor in competing businesses. Party A would favor this interpretation as it preserves most employment opportunities.\\n\\nClearer rewriting: 'For a period of two years following the Effective Date, Party A shall not, within the same city as Party B: (i) found, own, operate, or control any business that offers products or services similar to Party B's business; (ii) serve as an officer, director, or manager of any such business; (iii) provide consulting services to any such business; or (iv) own more than 5% equity interest in any such business. For clarity, employment in non-managerial positions with companies competing with Party B is not prohibited.'\\\"",
        'pt': "O bom prompt identifica especificamente onde reside a ambiguidade ('se envolver em qualquer negócio') e pede múltiplas interpretações (três), com análise estruturada de cada uma. Ao solicitar ao modelo que explique quais atividades seriam proibidas versus permitidas sob cada leitura, e qual parte favoreceria cada interpretação, o prompt incentiva uma análise equilibrada e completa de diferentes perspectivas. A solicitação de uma reescrita mais clara fornece valor prático além de apenas identificar o problema. Essa abordagem transforma o LLM em um parceiro de pensamento colaborativo que ajuda a antecipar argumentos potenciais de ambos os lados de uma disputa futura.\\\\n\\\\nExemplo de saída: \\\"Interpretação 1 (Mais Ampla): 'Envolver-se em qualquer negócio' proíbe a Parte A de qualquer envolvimento com negócios concorrentes, incluindo: emprego em qualquer nível, trabalho de consultoria, investimento passivo (mesmo participação minoritária) e, claro, fundar ou operar um negócio concorrente. Sob esta leitura, a Parte A ainda poderia trabalhar em setores não relacionados ou no mesmo setor fora da cidade especificada. A Parte B favoreceria essa interpretação, pois maximiza a proteção contra a concorrência.\\\\n\\\\nInterpretação 2 (Moderada): 'Envolver-se em qualquer negócio' significa participar ativamente da operação ou gestão de um negócio concorrente, incluindo: fundar uma empresa concorrente, atuar como executivo ou gerente, ou trabalhar em uma capacidade significativa que aproveite o conhecimento do setor. Sob esta leitura, a Parte A ainda poderia fazer investimentos passivos ou ocupar cargos não gerenciais em negócios concorrentes. Nenhuma das partes se beneficia claramente, pois isso representa um meio-termo.\\\\n\\\\nInterpretação 3 (Mais Restrita): 'Envolver-se em qualquer negócio' refere-se apenas a fundar, possuir ou controlar um negócio concorrente. Sob esta leitura, a Parte A seria proibida de iniciar seu próprio empreendimento concorrente ou ser acionista controlador, mas poderia trabalhar livremente como funcionário, consultor ou investidor minoritário em negócios concorrentes. A Parte A favoreceria essa interpretação, pois preserva a maioria das oportunidades de emprego.\\\\n\\\\nReescrita mais clara: 'Por um período de dois anos após a Data Efetiva, a Parte A não deverá, na mesma cidade que a Parte B: (i) fundar, possuir, operar ou controlar qualquer negócio que ofereça produtos ou serviços semelhantes aos negócios da Parte B; (ii) atuar como diretor, conselheiro ou gerente de qualquer negócio desse tipo; (iii) prestar serviços de consultoria a qualquer negócio desse tipo; ou (iv) possuir mais de 5% de participação acionária em qualquer negócio desse tipo. Para maior clareza, o emprego em cargos não gerenciais em empresas concorrentes da Parte B não é proibido.'\\\"",
    }
    technique8_resource_title = {
        'en': 'Using English-Language Contracts in China: My Q&A with China Law Blog',
        'pt': 'Usando Contratos em Inglês na China',
    }
    technique8_resource_url = 'https://www.adamsdrafting.com/using-english-language-contracts-in-china-my-q-and-a-with-china-law-blog/'
    technique8_resource_description = {
        'en': "Insights on cross-language contract interpretation challenges. Adam is just really good. If you ever read this, Adam, I'm your fan since 2011! (Update: Adam ignored my LinkedIn request...)",
        'pt': 'Insights sobre desafios de interpretação de contratos em diferentes idiomas. Adam é simplesmente ótimo. Se você algum dia ler isto, Adam, sou seu fã desde 2011! (Fui ignorado pelo Prof. Adam...)',
    }
    return


@app.cell
def _():
    # Cell: Define Technique 9
    technique9_slug = 'comparative-law'
    technique9_name = {
        'en': 'Comparative Law Analysis Across Jurisdictions',
        'pt': 'Análise Comparativa de Leis Entre Jurisdições',
    }
    technique9_description = {
        'en': 'Legal outcomes can vary dramatically across jurisdictions. A savvy prompt will recognize when a question requires a comparative approach and instruct the model to address each jurisdiction separately. This technique is useful for questions like, "How do the laws of the US and EU differ on data protection?" or "Compare patent eligibility in the US versus China." By explicitly naming the jurisdictions and requesting a structured comparison, you can obtain a clearer understanding of how different legal systems approach the same issue.',
        'pt': 'Os resultados legais podem variar dramaticamente entre jurisdições. Um prompt inteligente reconhece quando uma questão requer uma abordagem comparativa e instrui o modelo a abordar cada jurisdição separadamente. Esta técnica é útil para perguntas como, "Como as leis dos EUA e da UE diferem na proteção de dados?" ou "Compare a elegibilidade de patentes nos EUA versus China."',
    }
    technique9_why_it_works = {
        'en': 'Legal systems have fundamental differences in structure, principles, and priorities. Common law jurisdictions (like the US and UK) rely heavily on case precedent, while civil law systems (like Brazil and France) are grounded in comprehensive legal codes. When you explicitly name the jurisdictions and the specific legal issue at hand, you guide the model to access its knowledge about each distinct legal system rather than blending approaches. This technique acknowledges the reality of legal practice: that practitioners must consider the specific governing law of their case. Structured comparison also improves clarity, as the differences between jurisdictions become immediately apparent when presented side by side. Authoritative legal resources often present information in this comparative format precisely because it highlights key distinctions that might otherwise be lost in a generalized discussion.',
        'pt': 'Os sistemas jurídicos têm diferenças fundamentais em estrutura, princípios e prioridades. Jurisdições de common law (como EUA e Reino Unido) dependem fortemente de precedentes de casos, enquanto sistemas de direito civil (como Brasil e França) são fundamentados em códigos legais abrangentes. Ao nomear explicitamente as jurisdições e a questão jurídica específica, você orienta o modelo a acessar seu conhecimento sobre cada sistema jurídico distinto, em vez de misturar abordagens. Esta técnica reconhece a realidade da prática jurídica: que os profissionais devem considerar a lei específica que rege seu caso. A comparação estruturada também melhora a clareza, pois as diferenças entre jurisdições tornam-se imediatamente aparentes quando apresentadas lado a lado. Recursos jurídicos autoritativos frequentemente apresentam informações neste formato comparativo precisamente porque destaca distinções-chave que poderiam ser perdidas em uma discussão generalizada.',
    }
    technique9_example_question = {
        'en': 'Understanding how different jurisdictions treat penalty clauses in contracts. (You need advice on drafting penalty provisions that will be enforceable in multiple countries.)',
        'pt': 'Entender como diferentes jurisdições tratam cláusulas penais em contratos. (Você precisa de orientação para redigir disposições penais que sejam aplicáveis em vários países.)',
    }
    technique9_example_bad_prompt = {
        'en': 'Are penalty clauses in contracts enforceable?',
        'pt': 'As cláusulas penais em contratos são aplicáveis?',
    }
    technique9_example_good_prompt = {
        'en': 'Compare how penalty clauses in contracts are treated under New York law, English law, and Brazilian law. Outline the differences in enforceability and any legal limitations in each jurisdiction. Structure your response by jurisdiction, with clear headings, and include relevant legal principles or cases that inform the approach in each jurisdiction.',
        'pt': 'Compare como as cláusulas penais em contratos são tratadas segundo a lei de Nova York, a lei inglesa e a lei brasileira. Destaque as diferenças na aplicabilidade e quaisquer limitações legais em cada jurisdição. Estruture sua resposta por jurisdição, com títulos claros, e inclua princípios legais ou casos relevantes que informem a abordagem em cada jurisdição.',
    }
    technique9_example_explanation = {
        'en': "The good prompt explicitly names three jurisdictions (New York, England, and Brazil) and the specific legal concept (penalty clauses in contracts). It also requests a structured format with the jurisdictions clearly separated. This approach will yield a response that helps the user understand exactly how each legal system handles penalty clauses, rather than receiving a vague, generalized answer that might not apply in their situation.\\n\\nThe model's response would likely be organized by jurisdiction with clear distinctions highlighted. For New York and English law (both common law systems), the model would explain the strong prohibition against penalty clauses while allowing legitimate liquidated damages. For Brazilian law (a civil law system), it would note the different approach where penalty clauses are recognized and enforceable but subject to statutory limitations. The structured format makes these critical differences immediately apparent.\\n\\nThis comparative approach is particularly valuable for transactional lawyers drafting agreements that might be enforced in multiple jurisdictions. Without this clear comparison, a lawyer might draft provisions that would be unenforceable in some of the relevant jurisdictions. The prompt's request for relevant legal principles or cases also helps ensure the response includes authoritative support for each jurisdiction's approach, making the answer more reliable and trustworthy.\\n\\nExample output might include:\\n\\n**New York Law**\\n- Follows general common law principles - clauses deemed a \\\"penalty\\\" (punitive in nature) are not enforceable\\n- Courts distinguish between unenforceable penalty clauses and enforceable liquidated damages clauses\\n- Key test: Is the amount a reasonable pre-estimate of loss (enforceable) or punitive (unenforceable)?\\n- Courts will assess if the amount is disproportionate to the actual harm\\n\\n**English Law**\\n- Similar to New York, as the origin of the common law rule against penalties\\n- Leading case: Dunlop Pneumatic Tyre Co. v. New Garage (1915) established tests to distinguish penalties from genuine liquidated damages\\n- Modern development: Cavendish Square Holding v. Makdessi refined this test\\n- Core principle: If a clause imposes a detriment out of proportion to any legitimate interest in enforcement, it's an unenforceable penalty\\n\\n**Brazilian Law**\\n- Civil law approach differs significantly from common law jurisdictions\\n- The concept of a \\\"penalty clause\\\" (cláusula penal) is recognized and enforceable, but regulated by statute\\n- According to the Brazilian Civil Code, any contractual penalty cannot exceed the value of the main obligation\\n- Courts can reduce the penalty if deemed excessive or if there's partial performance\\n- Core difference: Brazil does not follow the common law penalty doctrine; it enforces agreed penalties within statutory limits",
        'pt': 'O bom prompt nomeia explicitamente três jurisdições (Nova York, Inglaterra e Brasil) e o conceito jurídico específico (cláusulas penais em contratos). Também solicita um formato estruturado com as jurisdições claramente separadas. Esta abordagem produzirá uma resposta que ajuda o usuário a entender exatamente como cada sistema jurídico lida com cláusulas penais, em vez de receber uma resposta vaga e generalizada que pode não se aplicar à sua situação.\\\\n\\\\nA resposta do modelo provavelmente seria organizada por jurisdição com distinções claras destacadas. Para a lei de Nova York e a lei inglesa (ambos sistemas de common law), o modelo explicaria a forte proibição contra cláusulas penais, permitindo danos liquidados legítimos. Para a lei brasileira (um sistema de direito civil), notaria a abordagem diferente onde as cláusulas penais são reconhecidas e aplicáveis, mas sujeitas a limitações estatutárias. O formato estruturado torna essas diferenças críticas imediatamente aparentes.\\\\n\\\\nEsta abordagem comparativa é particularmente valiosa para advogados transacionais que redigem acordos que podem ser aplicados em múltiplas jurisdições. Sem esta comparação clara, um advogado poderia redigir disposições que seriam inaplicáveis em algumas das jurisdições relevantes. A solicitação do prompt por princípios legais ou casos relevantes também ajuda a garantir que a resposta inclua suporte autoritativo para a abordagem de cada jurisdição, tornando a resposta mais confiável.\\\\n\\\\nExemplo de saída pode incluir:\\\\n\\\\n**Lei de Nova York**\\\\n- Segue princípios gerais de common law - cláusulas consideradas uma \\"penalidade\\" (de natureza punitiva) não são aplicáveis\\\\n- Tribunais distinguem entre cláusulas penais inaplicáveis e cláusulas de danos liquidados aplicáveis\\\\n- Teste chave: O montante é uma estimativa prévia razoável da perda (aplicável) ou punitivo (inaplicável)?\\\\n- Tribunais avaliarão se o montante é desproporcional ao dano real\\\\n\\\\n**Lei Inglesa**\\\\n- Semelhante a Nova York, como origem da regra de common law contra penalidades\\\\n- Caso principal: Dunlop Pneumatic Tyre Co. v. New Garage (1915) estabeleceu testes para distinguir penalidades de danos liquidados genuínos\\\\n- Desenvolvimento moderno: Cavendish Square Holding v. Makdessi refinou este teste\\\\n- Princípio central: Se uma cláusula impõe um detrimento desproporcional a qualquer interesse legítimo na execução, é uma penalidade inaplicável\\\\n\\\\n**Lei Brasileira**\\\\n- Abordagem de direito civil difere significativamente das jurisdições de common law\\\\n- O conceito de \\"cláusula penal\\" é reconhecido e aplicável, mas regulado por estatuto\\\\n- De acordo com o Código Civil Brasileiro, qualquer penalidade contratual não pode exceder o valor da obrigação principal\\\\n- Tribunais podem reduzir a penalidade se considerada excessiva ou se houver cumprimento parcial\\\\n- Diferença central: O Brasil não segue a doutrina de penalidade do common law; aplica penalidades acordadas dentro dos limites estatutários',
    }
    technique9_resource_title = {
        'en': 'Brazil Civil Code 2018 Amendments',
        'pt': 'Código Civil Brasileiro Emendas de 2018',
    }
    technique9_resource_url = 'https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect-qa/content/resources/attachments/brazil-law-civil-code-13.777-2018.pdf'
    technique9_resource_description = {
        'en': "Reference document showing Brazil's civil law approach to contract provisions",
        'pt': 'Documento de referência mostrando a abordagem do direito civil brasileiro para provisões contratuais',
    }
    return


@app.cell
def _(get_current_language, mo, translations):
    def generate_examples(bad_prompt_text, good_prompt_text):
        """Generate dropdown examples"""
        query_params = mo.query_params().to_dict()

        return mo.ui.dropdown(
            options={
                'Your prompt': {'prompt': ''},
                'Bad prompt': {'prompt': bad_prompt_text},
                'Good prompt': {'prompt': good_prompt_text},
            },
            value='Your prompt',
            label=translations['examples'][get_current_language()],
        )
    return (generate_examples,)


@app.cell
def _(get_current_language, mo, translations):
    # Cell 10: Create Interactive Playground
    def create_enhanced_interactive_playground(technique_name, bad_prompt, good_prompt):
        """
        Creates an interactive playground structure (without form values)
        """
        # Create the playground header
        playground_header = mo.md(f"""
        <div style="background-color: #000000; padding: 20px 40px; border: 2px solid #9D0208; margin-bottom: 15px;">
            <h3 style="color: #FFFFFF; margin-top: 0; margin-bottom: 10px; font-size: 1.2em; font-weight: 400; text-align: left; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase;">
                {translations['chat_experiment'][get_current_language()]}: <span style="color: #E5383B; font-weight: bold;">{technique_name[get_current_language()]}</span>
            </h3>
        </div>
        """)

        # Return components to be used by other cells
        return {
            'technique_name': technique_name,
            'bad_prompt': bad_prompt,
            'good_prompt': good_prompt,
            'header': playground_header,
        }
    return (create_enhanced_interactive_playground,)


@app.cell
def _(mo):
    # Cell 11: Output and Form Generation
    def generate_output(form, examples):
        """Generate output based on form submission or examples selection"""
        if form.value is not None:
            return mo.vstack(
                [
                    mo.md(
                        f"""
                        <div style="font-family: 'Inter', sans-serif; border: 2px solid #9D0208; border-radius: 0; padding: 15px; background-color: #F9F7F4;">
                            <h3 style="font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase; color: #D00000;">SELECTED PROMPT:</h3>
                            <pre style="white-space: pre-wrap; word-wrap: break-word; background-color: #000000; color: #FFFFFF; padding: 15px; border: 1px solid #E5383B;">{form.value}</pre>
                            <p style="font-style: italic; color: #9D0208;"><em>(RESULTS WILL BE AVAILABLE ON THE NEXT PAGE)</em></p>
                        </div>
                        """
                    )
                ]
            )
        return mo.vstack(
            [
                mo.md(
                    f"""
                    <div style="font-family: 'Inter', sans-serif; border: 2px solid #9D0208; border-radius: 0; padding: 15px; background-color: #F9F7F4;">
                        <h3 style="font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase; color: #D00000;">CURRENT SELECTION:</h3>
                        <pre style="white-space: pre-wrap; word-wrap: break-word; background-color: #000000; color: #FFFFFF; padding: 15px; border: 1px solid #E5383B;">{examples.value.get('prompt', '')}</pre>
                        <p style="font-style: italic; color: #9D0208;"><em>(RESULTS WILL BE AVAILABLE ON THE NEXT PAGE)</em></p>
                    </div>
                    """
                )
            ]
        )
    return (generate_output,)


@app.cell
def _(get_current_language, mo, translations):
    def generate_form(examples):  # Argument name matches calling code (e.g., examples1)
        """Generate form based on examples dropdown (handling dict value)"""
        lang = get_current_language()
        # examples.value is expected to be a dict like {'prompt': ...}
        selected_value_dict = examples.value
        initial_text_value = ''
        # Safely get the 'prompt' value from the dictionary
        if isinstance(selected_value_dict, dict):
            initial_text_value = selected_value_dict.get('prompt', '')

        return mo.ui.text_area(
            label=translations['your_prompt'][lang],
            placeholder=translations['enter_prompt_here'][lang],
            value=initial_text_value,
            full_width=True,
            rows=5,
        ).form(
            submit_button_label=translations['send_prompt'][lang],
            bordered=True,
            clear_on_submit=False,  # Keep text after submit for display_response
            show_clear_button=True,
        )
    return (generate_form,)


@app.cell
def _():
    technique10_slug = 'le-gran-finale'
    technique10_name = {
        'en': 'Le Gran Finalle: How do I use it and why you should too (or recency bias)',
        'pt': 'Le Gran Finale: Como eu uso e porque você deveria me imitar (ou o efeito de recência)',
    }

    technique10_description = {
        'en': "As cliché it sounds, prompting is a mix of art and technical approaches. The good thing is that language models are increasingly advanced, making even sloppy prompts somewhat workable. However, we lawyers value precision and excellence in our final outputs. Understanding how memory (context) works is crucial. Unlike fine wines, language models don't improve context comprehension with age--in fact, their memory mimics human old-age, showing a recency bias. Strategically positioning your critical instructions at the end of your prompt leverages this bias, significantly improving model compliance.",
        'pt': 'O efeito de recência é uma técnica poderosa de prompting que aproveita o viés de atenção de um LLM para informações colocadas no final do seu prompt. Ao posicionar estrategicamente suas instruções, exemplos ou restrições mais críticas no final do prompt, você aumenta dramaticamente a probabilidade de que sejam seguidos fielmente.',
    }

    technique10_why_it_works = {
        'en': "Despite their impressive capabilities, LLMs suffer from a very human-like memory limitation: they tend to forget earlier information in your prompt while hyperfocusing on the latest instructions. This isn't a flaw but a built-in consequence of how attention mechanisms operate within transformer architectures. The model allocates more resources to recent tokens, creating a recency bias that informed prompters can strategically exploit.",
        'pt': 'Apesar de suas capacidades impressionantes, os LLMs sofrem de uma limitação de memória muito semelhante à humana: eles tendem a esquecer o que foi mencionado no início do seu prompt enquanto hiperfocam no que veio por último. Isso não é uma falha de design, mas uma consequência de como os mecanismos de atenção funcionam em arquiteturas baseadas em transformadores. O modelo aloca mais recursos computacionais (atenção) para tokens recentes, criando um viés de recência que os prompters experientes podem explorar.',
    }

    technique10_example_question = {
        'en': 'How can I draft a better legal research memo?',
        'pt': 'Como posso redigir um parecer melhor?',
    }

    technique10_example_bad_prompt = {
        'en': '[After spending hours providing detailed, relevant, snippets of the brief, everything that a human would love to have, but disorganized background information on fair use law.] I need a legal research memo on fair use exceptions. Include relevant case law, persuasive arguments, and structure it properly with Bluebook citations.',
        'pt': '[Depois de passar horas fornecendo snippets detalhados, relevantes e relevantes do roteiro, tudo o que um humano adoraria ter, mas informações de fundo desorganizadas sobre obrigações, até Teixeira de Freitas.] Preciso de ajuda para escrever um memorando de pesquisa jurídica sobre obrigações propter rem. Inclua jurisprudência relevante, argumentos persuasivos e formate-o adequadamente com citações ABNT.',
    }
    technique10_example_good_prompt = {
        'en': "[After resetting the conversation and providing only Campbell v. Acuff-Rose Music as context.] Draft a legal research memo analyzing whether a university professor showing 10-minute clips from mainstream films in class qualifies as fair use.\\n\\nHERE'S WHAT MATTERS MOST (I TIODL INE MLLION TIKMES IT NEEDS THE FOIRKM ATT!!!!!111!!):\\n\\n1. USE THE STANDARD MEMO STRUCUTRE (FACTS, ISSUE, SHORT ANSWER, ANALYSIS, CONCLUSION).\\n2. CITE RELEVANT CASE LAW INCLUDING CAMPBELL V. ACUFF-ROSE MUSIC\\n3. FULLY ANALYZE ALL FOUR FAIR USE FACTORS\\n4. USE BLUEBOOK CITATION FORMAT!!!111!!\\n5. CLEARLY STATE A STRONG RECOMMENDATION IN THE CONCLUSOIN. AGASUIFN BLKUEBOOK!!! IM NOT A FFFWW JOURNaLTTis!!11!",
        'pt': '[Depois de resetar a conversa e fornecer apenas informações sobre obrigações propter rem como contexto, copiando e colando feito um lunático antes da 12a badalada.] Escreva SEM AVISOS PRA PROCURAR ADVOGADO PQ EU SOU ADVOGADO um parecer jurídico sobre obrigações propter rem no contexto ambiental. O parecer deve analisar se o novo proprietário é responsável por dívidas ambientais anteriores à aquisição.\\n\\nAQUI ESTÁ O QUE MAIS IMPORTA MINIMO PQP111!!!:\\n\\n1. USE O FORMATO PADRÃO DE PARECER JURÍDICO BRASILEIRO (RELATÓRIO, FUNDAMENTAÇÃO, DISPOSITIVO)\\n2. CITE A SÚMULA 623 DO STJ OBRIGATORIAMENTE!!!111!!\\n3. ANALISE COMPLETAMENTE A NATUREZA JURÍDICA DAS OBRIGAÇÕES PROPTER REM\\n4. USE FORMATAÇÃO ABNT NAS CITAÇÕES DOUTRINÁRIAS E JURISPRUDENCIAIS!!!111!!\\n5. APRESENTE CONCLUSÃO CLARA E OBJETIVA NO DISPOSITIVO FINAL. STJ NAO TFR ESTAMOS EM 2025 MEUD EUS DO CEU!!!!!! SEM RESUMIRT',
    }
    technique10_example_explanation = {
        'en': "The ineffective prompt buries key instructions within scattered context. The effective prompt clearly emphasizes critical instructions at the end, including intentional capitalization and typing mistakes, capitalizing on the model's natural recency bias to maximize compliance.",
        'pt': 'O prompt ineficaz mistura todos os requisitos sem ênfase. O prompt eficaz coloca instruções específicas no final em uma lista numerada visualmente distinta—exatamente onde a atenção do modelo é mais forte. Ao enfatizar os requisitos críticos com letras maiúsculas e posicioná-los no final, aumentamos drasticamente a probabilidade de execução fiel.',
    }

    technique10_resource_title = {
        'en': 'Lost in the Middle: How Language Models Use Long Contexts',
        'pt': 'Perdido no Meio: Como Modelos de Linguagem Usam Contextos Longos',
    }
    technique10_resource_url = 'https://arxiv.org/abs/2307.03172'
    technique10_resource_description = {
        'en': 'This paper from UC Berkeley researchers explores how information positioning within prompts affects language model responses, particularly highlighting the recency effect.',
        'pt': 'Este artigo acadêmico de pesquisadores da UC Berkeley examina como a posição das informações dentro de um prompt afeta significativamente a resposta de um modelo de linguagem, com atenção especial ao fenômeno do efeito de recência.',
    }
    return


@app.cell
def _(
    create_enhanced_interactive_playground,
    generate_examples,
    get_current_language,
):
    def create_interactive_playground_number(param):
        """
        Create playground components for a specific technique number
        """
        # Get the technique data
        playground_data = create_enhanced_interactive_playground(
            globals()[f'technique{param}_name'],
            globals()[f'technique{param}_example_bad_prompt'],
            globals()[f'technique{param}_example_good_prompt'],
        )

        # Generate examples dropdown
        examples = generate_examples(
            playground_data['bad_prompt'][get_current_language()],
            playground_data['good_prompt'][get_current_language()],
        )

        # Return data needed for the next cell
        return playground_data['header'], examples
    return (create_interactive_playground_number,)


@app.cell
def _(get_current_language, mo, translations):
    # Cell 9: Technique Data - Keeping function logic but styling the output
    def display_technique_(
        technique_slug,
        technique_name,
        technique_description,
        technique_why_it_works,
        technique_example_question,
        technique_example_bad_prompt,
        technique_example_good_prompt,
        technique_example_explanation,
        technique_resource_title,
        technique_resource_url,
        technique_resource_description,
    ):
        technique_header = mo.md(f"""
        <div id='{technique_slug}' style="margin-top: 5px;"></div>
        <div class="technique-header" style="background-color: #F9F7F4; padding: 40px 40px 0 40px; border-left: 5px solid #9D0208; margin-bottom: 0px; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; width: 100%; box-sizing: border-box;">
            <h2 style="color: #000000; margin-top: 0; margin-bottom: 2.5px; font-size: 1.5em; font-weight: 400; text-align: left; letter-spacing: 2px; text-transform: uppercase;">{technique_name[get_current_language()]}</h2>
            <p style="font-size: 1em; padding-top: 10px; margin: 0; color: #000000; font-weight: 200; text-align: left; padding-bottom: 15px; font-family: 'Inter', sans-serif;">{technique_description[get_current_language()]}</p>
            <hr style="border: 0; height: 2px; background: #9D0208; margin: 10px 0 20px 0;">
                <h3 style="color: #D00000; padding-bottom: 20px; font-size: 1.2em; margin: 0; font-weight: 400; text-align: center; letter-spacing: 2px; text-transform: uppercase;">
                {translations['issue'][get_current_language()]}: {technique_example_question[get_current_language()]}
            </h3>
        </div>
        """)

        example_tabs = mo.ui.tabs(
            {
                translations['without_technique'][get_current_language()]: mo.md(f"""
                <div class="technique-bad-example" style="background-color: #FFF; padding: 15px; border-radius: 0; border: 2px solid #9D0208; font-family: 'Inter', sans-serif;">
                    <h4 style="color: #D00000; margin-top: 0; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase;">{translations['without_technique'][get_current_language()]}</h4>
                    <div style="background-color: #F9F7F4; padding: 15px; border: 1px solid #E5383B; font-family: 'Inter', sans-serif;">
                        <p style="font-family: 'Inter', sans-serif;">{technique_example_bad_prompt[get_current_language()]}</p>
                    </div>
                </div>
                """),
                translations['with_technique'][get_current_language()]: mo.md(f"""
                <div class="technique-good-example" style="background-color: #FFF; padding: 15px; border-radius: 0; border: 2px solid #9D0208; font-family: 'Inter', sans-serif;">
                    <h4 style="color: #D00000; margin-top: 0; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase;">{translations['with_technique'][get_current_language()]}</h4>
                    <div style="background-color: #F9F7F4; padding: 15px; border: 1px solid #E5383B; font-family: 'Inter', sans-serif;">
                        <p style="font-family: 'Inter', sans-serif;">{technique_example_good_prompt[get_current_language()]}</p>
                    </div>
                </div>
                """),
                translations['explanation'][get_current_language()]: mo.md(f"""
                <div class="technique-explanation" style="background-color: #000000; padding: 15px; border-radius: 0; border: 2px solid #9D0208; font-family: 'Inter', sans-serif; color: #FFFFFF;">
                    <h4 style="color: #E5383B; margin-top: 0; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase;">{translations['explanation'][get_current_language()]}</h4>
                    <p style="font-family: 'Inter', sans-serif;">{technique_example_explanation[get_current_language()]}</p>
                </div>
                """),
            }
        )

        why_it_works_accordion = mo.accordion(
            {
                translations['why_it_works'][get_current_language()]: mo.md(f"""
                <div class="technique-why-it-works" style="padding: 15px; background-color: #000000; border-radius: 0; font-family: 'Inter', sans-serif; color: #FFFFFF; border: 2px solid #9D0208;">
                    <p style="color: #FFFFFF; font-family: 'Inter', sans-serif;">{technique_why_it_works[get_current_language()]}</p>
                </div>
                """)
            }
        )

        # Add more_resources accordion
        more_resources_accordion = mo.accordion(
            {
                'ADDITIONAL RESOURCES': mo.md(f"""
                <div class="technique-resources" style="padding: 15px; background-color: #000000; border-radius: 0; font-family: 'Inter', sans-serif; color: #FFFFFF; border: 2px solid #9D0208;">
                    <p style="color: #FFFFFF; font-family: 'Inter', sans-serif;">{technique_resource_description[get_current_language()]}</p>
                    <br>
                    <a href="{technique_resource_url}" target="_blank" style="color: #E5383B; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif; letter-spacing: 2px; text-transform: uppercase;">{technique_resource_title[get_current_language()]}</a>
                    <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(229, 56, 59, 0), rgba(229, 56, 59, 0.75), rgba(229, 56, 59, 0)); margin: 10px 0 0 0;">
                </div>
                """)
            }
        )
        components = [
            technique_header,
            example_tabs,
            why_it_works_accordion,
            more_resources_accordion,
        ]

        return mo.vstack(components)
    return (display_technique_,)


@app.cell
def display_technique_number(display_technique_):
    # Function to display a technique by number
    def display_technique_number(param):
        """
        Display a technique section using variables named with the given parameter number.

        Args:
            param: The technique number (1, 2, etc.)

        Returns:
            A marimo component displaying the technique section
        """
        return display_technique_(
                globals()[f'technique{param}_slug'],
                globals()[f'technique{param}_name'],
                globals()[f'technique{param}_description'],
                globals()[f'technique{param}_why_it_works'],
                globals()[f'technique{param}_example_question'],
                globals()[f'technique{param}_example_bad_prompt'],
                globals()[f'technique{param}_example_good_prompt'],
                globals()[f'technique{param}_example_explanation'],
                globals()[f'technique{param}_resource_title'],
                globals()[f'technique{param}_resource_url'],
                globals()[f'technique{param}_resource_description'],
            )
    return (display_technique_number,)


@app.cell
def _(display_technique_number):
    # Display technique #1
    display_technique_number(1)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #1
    header1, examples1 = create_interactive_playground_number(1)
    return examples1, header1


@app.cell
def _(examples1, generate_form):
    # Create form for technique #1
    form1 = generate_form(examples1)
    return (form1,)


@app.cell
def _(examples1, form1, generate_output):
    # Create output for technique #1
    output1 = generate_output(form1, examples1)
    return (output1,)


@app.cell
def _(examples1, form1, header1, mo, output1):
    # Assemble final UI for technique #1
    mo.vstack([header1, examples1, form1, output1], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form1):
    # Display response for technique #1
    display_response(form1)
    return


@app.cell
def _(display_technique_number):
    # Display technique #2
    display_technique_number(2)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #2
    header2, examples2 = create_interactive_playground_number(2)
    return examples2, header2


@app.cell
def _(examples2, generate_form):
    # Create form for technique #2
    form2 = generate_form(examples2)
    return (form2,)


@app.cell
def _(examples2, form2, generate_output):
    # Create output for technique #2
    output2 = generate_output(form2, examples2)
    return (output2,)


@app.cell
def _(examples2, form2, header2, mo, output2):
    # Assemble final UI for technique #2
    mo.vstack([header2, examples2, form2, output2], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form2):
    # Display response for technique #2
    display_response(form2)
    return


@app.cell
def _(display_technique_number):
    display_technique_number(3)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #3
    header3, examples3 = create_interactive_playground_number(3)
    return examples3, header3


@app.cell
def _(examples3, generate_form):
    # Create form for technique #3
    form3 = generate_form(examples3)
    return (form3,)


@app.cell
def _(examples3, form3, generate_output):
    # Create output for technique #3
    output3 = generate_output(form3, examples3)
    return (output3,)


@app.cell
def _(examples3, form3, header3, mo, output3):
    # Assemble final UI for technique #3
    mo.vstack([header3, examples3, form3, output3], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form3):
    # Display response for technique #3
    display_response(form3)
    return


@app.cell
def _(display_technique_number):
    display_technique_number(4)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #4
    header4, examples4 = create_interactive_playground_number(4)
    return examples4, header4


@app.cell
def _(examples4, generate_form):
    # Create form for technique #4
    form4 = generate_form(examples4)
    return (form4,)


@app.cell
def _(examples4, form4, generate_output):
    # Create output for technique #4
    output4 = generate_output(form4, examples4)
    return (output4,)


@app.cell
def _(examples4, form4, header4, mo, output4):
    # Assemble final UI for technique #4
    mo.vstack([header4, examples4, form4, output4], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form4):
    # Display response for technique #4
    display_response(form4)
    return


@app.cell
def _(display_technique_number):
    display_technique_number(5)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #5
    header5, examples5 = create_interactive_playground_number(5)
    return examples5, header5


@app.cell
def _(examples5, generate_form):
    # Create form for technique #5
    form5 = generate_form(examples5)
    return (form5,)


@app.cell
def _(examples5, form5, generate_output):
    # Create output for technique #5
    output5 = generate_output(form5, examples5)
    return (output5,)


@app.cell
def _(examples5, form5, header5, mo, output5):
    # Assemble final UI for technique #5
    mo.vstack([header5, examples5, form5, output5], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form5):
    # Display response for technique #5
    display_response(form5)
    return


@app.cell
def _(display_technique_number):
    # Display technique #6
    display_technique_number(6)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #6
    header6, examples6 = create_interactive_playground_number(6)
    return examples6, header6


@app.cell
def _(examples6, generate_form):
    # Create form for technique #6
    form6 = generate_form(examples6)
    return (form6,)


@app.cell
def _(examples6, form6, generate_output):
    # Create output for technique #6
    output6 = generate_output(form6, examples6)
    return (output6,)


@app.cell
def _(examples6, form6, header6, mo, output6):
    # Assemble final UI for technique #6
    mo.vstack([header6, examples6, form6, output6], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form6):
    # Display response for technique #6
    display_response(form6)
    return


@app.cell
def _(display_technique_number):
    display_technique_number(7)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #7
    header7, examples7 = create_interactive_playground_number(7)
    return examples7, header7


@app.cell
def _(examples7, generate_form):
    # Create form for technique #7
    form7 = generate_form(examples7)
    return (form7,)


@app.cell
def _(examples7, form7, generate_output):
    # Create output for technique #7
    output7 = generate_output(form7, examples7)
    return (output7,)


@app.cell
def _(examples7, form7, header7, mo, output7):
    # Assemble final UI for technique #7
    mo.vstack([header7, examples7, form7, output7], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form7):
    # Display response for technique #7
    display_response(form7)
    return


@app.cell
def _(display_technique_number):
    display_technique_number(8)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #8
    header8, examples8 = create_interactive_playground_number(8)
    return examples8, header8


@app.cell
def _(examples8, generate_form):
    # Create form for technique #8
    form8 = generate_form(examples8)
    return (form8,)


@app.cell
def _(examples8, form8, generate_output):
    # Create output for technique #8
    output8 = generate_output(form8, examples8)
    return (output8,)


@app.cell
def _(examples8, form8, header8, mo, output8):
    # Assemble final UI for technique #8
    mo.vstack([header8, examples8, form8, output8], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form8):
    # Display response for technique #8
    display_response(form8)
    return


@app.cell
def _(display_technique_number):
    display_technique_number(9)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #9
    header9, examples9 = create_interactive_playground_number(9)
    return examples9, header9


@app.cell
def _(examples9, generate_form):
    # Create form for technique #9
    form9 = generate_form(examples9)
    return (form9,)


@app.cell
def _(examples9, form9, generate_output):
    # Create output for technique #9
    output9 = generate_output(form9, examples9)
    return (output9,)


@app.cell
def _(examples9, form9, header9, mo, output9):
    # Assemble final UI for technique #9
    mo.vstack([header9, examples9, form9, output9], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form9):
    # Display response for technique #9
    display_response(form9)
    return


@app.cell
def _(display_technique_number):
    display_technique_number(10)
    return


@app.cell
def _(create_interactive_playground_number):
    # Create components for technique #10
    header10, examples10 = create_interactive_playground_number(10)
    return examples10, header10


@app.cell
def _(examples10, generate_form):
    # Create form for technique #10
    form10 = generate_form(examples10)
    return (form10,)


@app.cell
def _(examples10, form10, generate_output):
    # Create output for technique #10
    output10 = generate_output(form10, examples10)
    return (output10,)


@app.cell
def _(examples10, form10, header10, mo, output10):
    # Assemble final UI for technique #10
    mo.vstack(
        [header10, examples10, form10, output10], justify='space-between', heights=[1, 2, 1, 1]
    )
    return


@app.cell
def _(display_response, form10):
    # Display response for technique #10
    display_response(form10)
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        <div style="display: flex; flex-direction: column; align-items: center; padding: 30px 0; position: relative; border-top: 2px solid #9D0208; background: #F9F7F4; width: 100%;">
            <div style="position: relative; width: 100%; display: flex; flex-direction: column; align-items: center; padding: 0 20px">
                <div style="font-size: 16px; letter-spacing: 5px; color: #D00000; margin-bottom: 5px; text-align: center; font-family: 'Bebas Neue', Helvetica, Arial, sans-serif;">
                    Thanks!
                </div>

                <div style="font-size: 18px; margin-top: 15px; color: #333; text-align: center; font-family: 'Inter', sans-serif;">
                    If you found errors or have any suggestions, <a href="mailto:arthrod@umich.edu" style="color: #9D0208; text-decoration: none; font-weight: bold;">LET ME KNOW</a>
                </div>
                <div style="width: 50px; height: 5px; background: #9D0208; margin: 20px 0"></div>
                <div style="display: flex; align-items: center">


                    <div style="padding: 0 10px; font-size: 16px; color: #333; font-family: 'Inter', sans-serif;">Made with ❤️ by Arthur Souza Rodrigues</div>

                </div>
            </div>
        </div>
        """
    )
    return


if __name__ == "__main__":
    app.run()
