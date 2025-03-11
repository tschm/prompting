import marimo

__generated_with = "0.11.17"
app = marimo.App(layout_file="layouts/app.slides.json", css_file="custom.css")


@app.cell(hide_code=True)
def _():
    # Cell 1: Imports & Setup
    import marimo as mo
    import os
    import json
    import httpx

    from typing import List, Dict, Any, Optional

    # We'll keep a response cache to avoid regenerating the same prompts:
    response_cache = {}
    return Any, Dict, List, Optional, httpx, json, mo, os, response_cache


@app.cell
def _(Optional, httpx, json, os):
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
                self.api_key = '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'
                if not self.api_key:
                    raise ValueError('OPENAI_API_KEY environment variable not set')
                self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.api_key}'}
                self.endpoint = 'https://openrouter.ai/api/v1/chat/completions'
                self.default_model = 'openai/gpt-4o-mini'

            elif self.provider == 'anthropic':
                self.api_key = os.environ.get('ANTHROPIC_API_KEY')
                if not self.api_key:
                    raise ValueError('ANTHROPIC_API_KEY environment variable not set')
                self.headers = {'Content-Type': 'application/json', 'x-api-key': self.api_key, 'anthropic-version': '2023-06-01'}
                self.endpoint = 'https://api.anthropic.com/v1/messages'
                self.default_model = 'claude-3-haiku-20240307'

            else:
                raise ValueError(f'Unsupported provider: {provider}')

        def generate(
            self, prompt: str, system_message: str = 'You are a helpful assistant.', model: Optional[str] = None, temperature: float = 0.7
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
                        'messages': [{'role': 'system', 'content': system_message}, {'role': 'user', 'content': prompt}],
                        'temperature': temperature,
                    }

                    response = self.client.post(self.endpoint, headers=self.headers, json=payload)

                    response.raise_for_status()
                    data = response.json()
                    return data['choices'][0]['message']['content']

                elif self.provider == 'anthropic':
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


    # Example usage in a Marimo notebook:
    #
    # # Method 1: Using our custom client
    # import os
    # os.environ["OPENAI_API_KEY"] = "your-api-key-here"  # Set this securely
    #
    # client = DirectLLMClient(provider="openai")
    # response = client.generate(
    #     prompt="Explain how to use pandas for time series analysis",
    #     system_message="You are a data science expert."
    # )
    #
    # display_response("Explain how to use pandas for time series analysis", response)
    #
    # # Method 2: An even simpler fallback using Python's built-in libraries
    # def simple_openai_request(prompt, system_message="You are a helpful assistant."):
    #     """Ultra-simple OpenAI request using just the standard library."""
    #     import os
    #     import json
    #     import urllib.request
    #
    #     api_key = os.environ.get("OPENAI_API_KEY")
    #     if not api_key:
    #         return "Error: OPENAI_API_KEY environment variable not set"
    #
    #     url = "https://api.openai.com/v1/chat/completions"
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": f"Bearer {api_key}"
    #     }
    #     data = {
    #         "model": "gpt-3.5-turbo",
    #         "messages": [
    #             {"role": "system", "content": system_message},
    #             {"role": "user", "content": prompt}
    #         ],
    #         "temperature": 0.7
    #     }
    #
    #     # Create the request
    #     request = urllib.request.Request(
    #         url,
    #         data=json.dumps(data).encode('utf-8'),
    #         headers=headers,
    #         method="POST"
    #     )
    #
    #     try:
    #         # Send the request and get the response
    #         with urllib.request.urlopen(request) as response:
    #             response_data = json.loads(response.read().decode('utf-8'))
    #             return response_data["choices"][0]["message"]["content"]
    #     except Exception as e:
    #         return f"Error: {str(e)}"
    return (DirectLLMClient,)


@app.cell(hide_code=True)
def _(mo):
    get_submissions, set_submissions = mo.state([])
    get_prompt, set_prompt = mo.state('')
    return get_prompt, get_submissions, set_prompt, set_submissions


@app.cell(hide_code=True)
def _(mo):
    language_is_english = mo.ui.checkbox(label='Language is English', value=True)
    return (language_is_english,)


@app.cell(hide_code=True)
def _(language_is_english):
    def get_current_language():
        """Returns 'en' if language switch is set to English, otherwise 'pt'."""
        return 'en' if language_is_english.value else 'pt'
    return (get_current_language,)


@app.cell(hide_code=True)
def _():
    # Cell 3: Translations
    translations = {
        'language_toggle': {'en': 'Language', 'pt': 'Idioma'},
        'english': {'en': 'English', 'pt': 'Inglês'},
        'portuguese': {'en': 'Portuguese', 'pt': 'Português'},
        'welcome_title': {
            'en': 'Prompting Techniques Interactive Exercises',
            'pt': 'Exercícios Interativos de Técnicas de Prompt',
        },
        'welcome_description': {
            'en': "This notebook demonstrates prompting techniques using Marimo and Anthropic's Claude model.",
            'pt': 'Este notebook demonstra técnicas de prompt usando Marimo e o modelo Claude da Anthropic.',
        },
        'issue': {'en': 'Issue', 'pt': 'Problema'},
        'examples': {'en': 'Examples', 'pt': 'Exemplos'},
        'without_technique': {'en': 'Without Technique', 'pt': 'Sem a Técnica'},
        'with_technique': {'en': 'With Technique', 'pt': 'Com a Técnica'},
        'prompt': {'en': 'Prompt', 'pt': 'Prompt'},
        'get_response': {'en': 'Get Response', 'pt': 'Obter Resposta'},
        'generating': {'en': 'Generating response...', 'pt': 'Gerando resposta...'},
        'response': {'en': 'Response:', 'pt': 'Resposta:'},
        'explanation': {'en': 'Why this works better', 'pt': 'Por que isso funciona melhor'},
        'why_it_works': {'en': 'Why this technique works', 'pt': 'Por que esta técnica funciona'},
        'additional_resources': {'en': 'Additional Resources', 'pt': 'Recursos Adicionais'},
        'chat_experiment': {'en': 'Try it yourself', 'pt': 'Experimente você mesmo'},
        'your_prompt': {'en': 'Your prompt', 'pt': 'Seu prompt'},
        'enter_prompt_here': {'en': 'Enter your prompt here...', 'pt': 'Digite seu prompt aqui...'},
        'inject_bad_prompt': {'en': 'Use Bad Prompt', 'pt': 'Usar Prompt Ruim'},
        'inject_good_prompt': {'en': 'Use Good Prompt', 'pt': 'Usar Prompt Bom'},
        'send_prompt': {'en': 'Send Prompt', 'pt': 'Enviar Prompt'},
        'table_of_contents': {'en': 'Table of Contents', 'pt': 'Índice'},
        'using_api_key': {'en': '✓ Using Anthropic API key from environment', 'pt': '✓ Usando chave de API da Anthropic do ambiente'},
        'enter_api_key': {'en': 'Enter your Anthropic API key', 'pt': 'Digite sua chave de API da Anthropic'},
        'api_key_placeholder': {'en': 'Enter your API key here', 'pt': 'Digite sua chave de API aqui'},
    }
    return (translations,)


@app.cell
def _(mo):
    mo.md(
        """
        <div style="display: flex; align-items: center; margin-bottom: 20px; padding: 50px 20px 40px 40px; background-color: #f0f4f8; border-left: 5px solid #4a5568; width: 100%; box-sizing: border-box; font-family: 'EB Garamond', 'Garamond', serif;">
            <div style="width: 100%;">
                <h1 style="margin: 0; color: #000000; text-align: left; font-weight: 400; padding-left: 0;">Prompting Techniques for Attorneys</h1>
                <p style="margin: 0; padding-top: 10px; color: #000000; text-align: left; font-weight: 200; padding-left: 0;">Learn how to craft effective prompts for AI language models</p>
                <p style="text-align: right; margin-top: 15px; padding-right: 20px;">By <a href="https://synthetic.lawyer" style="color: #4a5568; text-decoration: none;">Arthur Souza Rodrigues</a></p>
            </div>
        </div>
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        """
        <div style="display: flex; align-items: center; margin-bottom: 0px; padding: 50px 20px 0px 40px; background-color: #f0f4f8; border-left: 5px solid #4a5568; width: 100%; box-sizing: border-box; font-family: 'EB Garamond', 'Garamond', serif;">
            <div style="width: 100%;">
                <h1 style="margin: 0; color: #000000; text-align: left; font-weight: 400;">Welcome!</h1>
            </div>
        </div>

        <div style="padding: 30px 20px; background-color: #f0f4f8; margin-top: 0; font-family: 'Garamond', serif; border-left: 5px solid #4a5568;">
            <p><strong>Hey there!</strong></p>
            <p>I know, I know, you already regret clicking this link. But you can't resist the temptation to procrastinate. I'm giving you an excellent reason, please be thankful.</p>
            <p>This is an ✨interactive✨ notebook, split in err... too many lessons. The goal is to dig in a bit more, so you can pretend (like me), that you really studied hard all those papers and understand the reason behind the format. The same level of our bar exam preparation course (10 years for me, ouch!).</p>
            <p>You will have a general rule, a use-case, then an example of a bad and a good prompt. Then why the good is good or amazing, or less bad.</p>
            <p>Then, if you reeeeeally want to spend your time, we have two clickable accordions (the thingy below the tabs), one giving more information and the other providing theoretical or experience support.</p>

            <h3 style="color: #333; margin-top: 20px;">What You'll Learn Today:</h3>
            <ol>
                <li><strong>Role-Based Prompts</strong> - Make the AI think it graduated top of its class at Harvard Law</li>
                <li><strong>Context-Rich Instructions</strong> - Because models can't read your mind (yet!)</li>
                <li><strong>Constraint-Based Commands</strong> - For when you want JUST the termination clause, not the entire 50-page agreement</li>
                <li><strong>Example-Driven Templates</strong> - Show, don't tell (just like that partner who never explains what they want)</li>
                <li><strong>Step-by-Step Legal Analysis</strong> - Force the AI to show its work like your 1L professor</li>
                <li><strong>Contract Extraction Wizardry</strong> - Getting the needle from the haystack without the haystack</li>
                <li><strong>MSA Clause Drafting</strong> - Making clauses that won't make your GC cry</li>
                <li><strong>Ambiguity Handling</strong> - Because legal language is confusing (on purpose!)</li>
                <li><strong>Comparative Law Techniques</strong> - For when one jurisdiction isn't complicated enough</li>
                <li><strong>Le Gran Finale</strong> - The SURPRISE technique! Placing critical instructions at the end ...</li>
            </ol>

            <p style="margin-top: 20px;">Each technique comes with real-world examples of what works, what flops, and why. By the end, you'll be extracting genuinely useful legal analysis instead of whatever that thing is the AI usually gives you on the first try. Or maybe you will get even worse results, I can't guarantee.</p>
            <p>Also, to torture you well tortured souls, after each section you will be able to test your ✨deepmind deepknowledge deepresearch✨ mind.</p>
            <p>In all seriousness, I'm confident this will be useful to you and I hope it actually is!</p>

            <p style="margin-top: 20px;">Best,<br>Arthur</p>
            <p>Ps. Hey! If you read this, follow me on <a href="https://www.linkedin.com/in/arthrod/detail/recent-activity/" style="color: #4267B2; text-decoration: none;">LinkedIn</a>, pretty please?</p>
            <p>Ps2. Yes, Claude corrected me on 'Le Gran Finale.' But just to prove that I wrote this myself (I mean, kind off), I decided to leave as is.</p>
        </div>
        """
    )
    return


@app.cell(hide_code=True)
def _():
    # Cell 7: Technique Data
    technique1_slug = 'persona'
    technique1_name = {'en': 'Role-Based Prompting (Persona Priming)', 'pt': 'Prompting Baseado em Papéis (Preparação de Persona)'}
    technique1_description = {
        'en': 'Role-based prompting involves explicitly assigning the AI a specific role or persona relevant to the task. For example, you might begin a prompt with "You are an experienced contracts attorney…" or "Act as a judge writing an opinion…". This primes the model to adopt the perspective, knowledge, and tone of that role. It can also include defining the audience or viewpoint (e.g. "explain like I\'m a client" vs. "write as a legal scholar"). By setting a persona, the prompt guides the LLM to produce answers aligned with that expertise or viewpoint.',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique1_why_it_works = {
        'en': 'Specifying a role focuses the LLM on domain-specific knowledge and style, narrowing the scope of its response. Authoritative guidance suggests treating the LLM "as a brilliant but very new employee…who needs explicit instructions," which includes giving it a clear role. Research has shown that responses can improve in accuracy when the prompt asks for analysis in the voice of a particular expert; for instance, GPT-4 gave a correct answer when asked to analyze a case "as [Harvard Law Professor] Cass Sunstein might," whereas a generic prompt yielded a hallucination. In practice, a persona provides context that the model can implicitly use (such as legal terminology or methodology familiar to that role), resulting in more on-point and technically accurate answers.',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique1_example_question = {
        'en': "A client's supplier breached a contract. What should the client do?",
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique1_example_bad_prompt = {
        'en': 'What should a company do if a supplier breaks a contract?',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique1_example_good_prompt = {
        'en': "You are a seasoned contracts attorney advising a tech company. The company's supplier failed to deliver goods, breaching their contract. Explain the legal steps the company should take next (e.g. sending a breach notice, seeking damages under the contract or UCC), in plain language for a business executive.",
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique1_example_explanation = {
        'en': 'By assigning the AI the role of a "seasoned contracts attorney," the model focuses on providing legally sound advice about contract breaches. The prompt also specifies the audience (a business executive), which guides the AI to use "plain language" while still covering technical legal concepts like breach notices and UCC remedies. The resulting response is likely to include structured legal steps, appropriate citations to relevant law, and practical advice—all delivered in the professional tone of an attorney advising a client. Without this role priming, the response might lack legal specificity or fail to address formal remedies available under contract law.',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique1_resource_title = {'en': 'GenAI Prompting Tips for Lawyers', 'pt': '[Placeholder for Portuguese translation]'}
    technique1_resource_url = 'https://cl.cobar.org/departments/genai-prompting-tips-for-lawyers/'
    technique1_resource_description = {
        'en': 'Comprehensive guide on effective prompting techniques for legal professionals',
        'pt': '[Placeholder for Portuguese translation]',
    }
    return (
        technique1_description,
        technique1_example_bad_prompt,
        technique1_example_explanation,
        technique1_example_good_prompt,
        technique1_example_question,
        technique1_name,
        technique1_resource_description,
        technique1_resource_title,
        technique1_resource_url,
        technique1_slug,
        technique1_why_it_works,
    )


@app.cell(hide_code=True)
def _():
    # Cell: Technique 2 Definition
    technique2_slug = 'context-rich'
    technique2_name = {'en': 'Context-Rich Prompting (Including Details and Background)', 'pt': 'Placeholder for Portuguese translation'}
    technique2_description = {
        'en': 'Context-rich prompting means supplying the LLM with all relevant background facts, documents, and parameters of the query. Rather than asking a question in isolation, you include essential details such as the jurisdiction, involved parties, key facts, and the specific legal issue at hand. For instance, instead of "Can I fire an employee for social media posts?", you would ask, "As an employer in California, can I lawfully fire an at-will employee who posted negative comments about our company on social media?". You might also provide the text of a law or contract clause if interpretation is needed. By giving this specific context, you reduce ambiguity and guide the AI to consider the correct factual and legal framework.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique2_why_it_works = {
        'en': "LLMs do not have the ability to ask clarifying questions; they rely entirely on the prompt to understand the situation. Providing detailed context closes knowledge gaps and prevents the AI from making incorrect assumptions. Ambiguous or overly broad prompts can lead to irrelevant or wrong answers, whereas detailed prompts yield more tailored and accurate results. In fact, experts note that the more elaborate and specific the prompt (goals, facts, desired output, tone), the better the results. Including context like the type of case, relevant dates, jurisdiction, or document excerpts focuses the model on the correct scenario and laws, much like how a lawyer frames an issue before analysis. This technique ensures the AI's answer is grounded in the scenario you care about, rather than a generic summary of the law.",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique2_example_question = {
        'en': 'An HR manager wants legal advice on firing an employee over social media posts. (The legality can depend on context like jurisdiction and circumstances.)',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique2_example_bad_prompt = {
        'en': 'Can I fire an employee for what they said on social media?',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique2_example_good_prompt = {
        'en': 'You are an employment lawyer advising a manager in California. The company is considering firing an at-will employee who posted critical comments about the company on Facebook after work hours. Provide an analysis of whether this termination would be legal under California law, considering any free speech or labor law protections.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique2_example_explanation = {
        'en': "By identifying both the jurisdiction (California) and the employment context (at-will employment, social media post, off-duty conduct), the prompt guides the LLM to apply California-specific law and relevant statutes. It also specifies the angle of analysis (legal protections for the employee's speech vs. the employer's rights). This contextual information helps the AI deliver a more nuanced, legally accurate answer that references specific state laws rather than providing generic advice. The output would include references to California Labor Code § 96(k) and § 98.6 which protect employees' speech and activities, as well as considerations under the National Labor Relations Act if the posts could be considered concerted activity about workplace conditions. The response would be tailored to California's specific legal framework rather than giving generic advice.",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique2_resource_title = {'en': 'Writing Effective Legal AI Prompts', 'pt': 'Placeholder for Portuguese translation'}
    technique2_resource_url = 'https://legal.thomsonreuters.com/blog/writing-effective-legal-ai-prompts/'
    technique2_resource_description = {
        'en': 'Thomson Reuters guide on crafting effective prompts for legal AI applications',
        'pt': 'Placeholder for Portuguese translation',
    }
    return (
        technique2_description,
        technique2_example_bad_prompt,
        technique2_example_explanation,
        technique2_example_good_prompt,
        technique2_example_question,
        technique2_name,
        technique2_resource_description,
        technique2_resource_title,
        technique2_resource_url,
        technique2_slug,
        technique2_why_it_works,
    )


@app.cell(hide_code=True)
def _():
    # Cell: Define Technique 3
    technique3_slug = 'constraint-based'
    technique3_name = {'en': 'Constraint-Based Prompting (Conditional and Focused Instructions)'}
    technique3_description = {
        'en': 'Constraint-based prompting introduces explicit conditions or limits into your prompt to narrow the scope of the AI\'s response. This can take the form of conditional instructions (e.g., "If X is true, do Y; if not, say it\'s not applicable.") or other constraints like word limits, format requirements, or focusing on a specific subsection of content. The goal is to have the LLM only address a particular area or follow certain rules, rather than responding broadly. For example, when analyzing a lengthy contract, you might write: "If the contract contains a termination clause, summarize that clause. Ignore other provisions." Similarly, you can constrain output length ("in 100 words") or style ("list 3 key points"). By setting clear boundaries or prerequisites in the prompt, you guide the model to produce a more targeted answer.',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique3_why_it_works = {
        'en': 'Constraints help narrow down the AI\'s focus so it doesn\'t stray into irrelevant territory. Large language models will try to use everything in the prompt to generate an answer, so if you tell it exactly what not to do or what specific subset to concentrate on, you reduce noise and off-point results. Legal professionals often only need certain information (for instance, just the holding of a case, or just one contract clause) — constraints ensure the AI filters its output to those needs. Authoritative sources recommend setting conditions or scope in prompts to make the analysis "contextually appropriate and relevant to your needs," thereby cutting out unnecessary results. Additionally, adding constraints like length or format limits can improve clarity; it forces the model to be concise and stick to the requested structure. In essence, constraint-based prompting is about precision: it directs the LLM to comply with specific requirements, much like a lawyer telling a junior associate, "Give me only the relevant facts on X and nothing else."',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique3_example_question = {
        'en': 'Summarizing a specific part of a contract. (The user has a long employment contract but only cares about termination terms.)',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique3_example_bad_prompt = {'en': 'Summarize this employment contract.', 'pt': '[Placeholder for Portuguese translation]'}
    technique3_example_good_prompt = {
        'en': 'If the following employment contract contains a Termination or Severance clause, summarize those provisions in detail, focusing only on termination conditions and any severance pay terms. If not, respond that the contract has no such provisions. Ignore other sections.',
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique3_example_explanation = {
        'en': "The prompt explicitly sets a condition and scope: it tells the AI to look for termination or severance clauses and report on those and nothing else. It also provides a conditional fallback (\"if not, say there are none\") so the AI won't wander off-topic if the condition isn't met. This focused instruction ensures the AI's output will directly address the user's need (termination terms) without extraneous contract details. It also implicitly instructs the AI to read the contract text (provided in the prompt) with an eye only for a specific subject, which is akin to running a targeted search within the text.\n\nExample output: \"Termination Clause (Section 5): The contract allows either party to terminate with 30 days' written notice. However, if the employee is terminated for cause (defined as gross misconduct or violation of company policy), the employer can terminate immediately without notice. The clause specifies that termination must be communicated in writing and outlines a post-termination non-compete period of 6 months.\n\nSeverance Provision (Section 6): In cases of termination without cause, the employee is entitled to a severance payment equal to 3 months' salary. The severance is conditioned on the employee signing a release of claims. No severance is given if the termination is for cause or if the employee resigns.\"",
        'pt': '[Placeholder for Portuguese translation]',
    }
    technique3_resource_title = {'en': 'Prompt Engineering and Priming in Law', 'pt': '[Placeholder for Portuguese translation]'}
    technique3_resource_url = 'https://www.researchgate.net/publication/382878312_Prompt_Engineering_and_Priming_in_Law'
    technique3_resource_description = {
        'en': 'Research on effective prompt engineering techniques for legal applications',
        'pt': '[Placeholder for Portuguese translation]',
    }
    return (
        technique3_description,
        technique3_example_bad_prompt,
        technique3_example_explanation,
        technique3_example_good_prompt,
        technique3_example_question,
        technique3_name,
        technique3_resource_description,
        technique3_resource_title,
        technique3_resource_url,
        technique3_slug,
        technique3_why_it_works,
    )


@app.cell(hide_code=True)
def _():
    # Cell: Technique 4 Definition
    technique4_slug = 'example-few-shot'
    technique4_name = {
        'en': 'Example (Few-Shot) Prompting (Providing Exemplars or Templates)',
        'pt': 'Prompt por Exemplos (Few-Shot) (Fornecimento de Exemplares ou Modelos)',
    }
    technique4_description = {
        'en': "Example prompting, also known as few-shot prompting, involves including sample inputs/outputs or a template in your prompt to demonstrate the desired format, style, or level of detail. This can mean giving the AI one or more Q&A examples before your actual question, or providing a model answer structure. In the legal context, you might show an example of a well-written clause, then ask the AI to draft a similar clause for a new scenario. For instance: \"Example – Clause: 'In the event of breach, the non-breaching party shall… [legal language] …' Now draft a liability waiver clause for a service contract in a similar style.\" Another use is to provide a few sample legal questions with correct answers (few-shot Q&A) before posing a new question, which primes the model on the approach. By doing so, you leverage the AI's pattern recognition strength: it will mimic the structure or reasoning of the examples when generating the new answer.",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique4_why_it_works = {
        'en': 'Large language models learn and operate by recognizing patterns. When you provide a sample of a good response, you essentially program the model with a mini example of the task at hand. The model will infer the style, tone, and logic from the example and apply it to the new prompt. This few-shot prompting technique is well-documented to improve performance, especially for niche tasks or formats that the model might not guess on its own. Instead of relying on the AI to deduce the desired output style, you show it explicitly. Authoritative guidelines for legal AI suggest offering a template or bullet-point structure to guide the AI\'s response. For example, telling the model, "Follow this structure: 1) Facts, 2) Issue, 3) Holding" can lead to an answer in that format. Similarly, providing a placeholder-filled template (e.g., using bracketed placeholders in an example contract clause) lets the AI know exactly how to format the answer. By demonstration, we reduce ambiguity — the AI doesn\'t have to "figure out" the format or level of detail, it just continues the pattern. This results in output that is closer to the user\'s expected answer in both form and substance.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique4_example_question = {
        'en': 'Drafting a contract clause with a specific style. (The user wants a liability waiver clause similar to an example they like.)',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique4_example_bad_prompt = {
        'en': '"Draft a liability waiver clause for a service contract."',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique4_example_good_prompt = {
        'en': '"Draft a liability waiver clause for a service contract. Use the following clause as a style guide and follow a similar structure and tone:\n\nExample Clause: "In no event shall [Party] be liable for any indirect, incidental, or consequential damages arising out of or related to this Agreement, except in cases of gross negligence or willful misconduct…"\n\nNow, write the liability waiver for our contract in a similar style, adjusting details for our context (a software service provider)."',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique4_example_explanation = {
        'en': 'The good prompt provides a concrete example clause that demonstrates the desired style (it\'s concise, includes a standard exclusion of indirect damages, and has an exception for gross negligence). By instructing the AI to use it as a guide, the model will mirror that phrasing and structure when drafting the new clause. The prompt also specifies the context (software service provider) so the AI can adjust any particulars (for instance, referencing "software or data" in the waiver if relevant). This approach reduces the guesswork for the AI – it knows exactly the kind of clause the user wants, resulting in a clause that likely aligns with industry standards or the user\'s preference as shown in the example.\n\nExample output: "Liability Waiver Clause: In no event shall either party be liable to the other for any indirect, special, incidental, or consequential damages (including lost profits or data loss) arising out of or related to this Agreement or the services provided, even if such party has been advised of the possibility of such damages. The foregoing limitation applies to all causes of action, whether arising in contract, tort, or otherwise, except that nothing in this Agreement shall limit or exclude liability for a party\'s gross negligence or willful misconduct."\n\nThe output clause closely follows the style of the example: it uses the "In no event shall…" phrasing, disclaims indirect damages, and includes an exception for gross negligence/willful misconduct. By contrast, a clause generated without the example might have been structured differently or missed including the exception. The example prompt ensured the result was aligned with the desired template.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique4_resource_title = {'en': 'Minnesota Law Review Article on LLMs in Legal Practice', 'pt': 'Placeholder for Portuguese translation'}
    technique4_resource_url = 'https://minnesotalawreview.org/wp-content/uploads/2023/10/FL1-Choi-Schwarcz.pdf'
    technique4_resource_description = {
        'en': 'Comprehensive exploration of few-shot prompting techniques in legal contexts',
        'pt': 'Placeholder for Portuguese translation',
    }
    return (
        technique4_description,
        technique4_example_bad_prompt,
        technique4_example_explanation,
        technique4_example_good_prompt,
        technique4_example_question,
        technique4_name,
        technique4_resource_description,
        technique4_resource_title,
        technique4_resource_url,
        technique4_slug,
        technique4_why_it_works,
    )


@app.cell(hide_code=True)
def _():
    technique5_slug = 'step-by-step'
    technique5_name = {'en': 'Step-by-Step Prompting (Chain-of-Thought Legal Reasoning)', 'pt': 'Placeholder for Portuguese translation'}
    technique5_description = {
        'en': 'Step-by-step prompting involves asking the LLM to work through the problem in a logical sequence, rather than jumping straight to a conclusion. In legal tasks, this often means prompting the model to apply a structured analysis (for example, the IRAC method: Issue, Rule, Application, Conclusion, or breaking down elements of a legal test). You can achieve this by explicitly instructing the AI how to structure its reasoning. For instance: "Analyze this scenario step by step: first identify the legal issues, then state the relevant law for each issue, apply the facts, and finally give a conclusion." or simply "Let\'s think this through step-by-step.". Another variant is telling the model to enumerate its reasoning (e.g., "1, 2, 3…"). The idea is to mimic how a lawyer would deliberate on a problem methodically. This technique is especially useful for complex scenarios with multiple factors (such as determining if negligence is present, which requires analyzing duty, breach, causation, damages in turn).',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique5_why_it_works = {
        'en': 'Prompting an LLM to show its work leads to more transparent and often more accurate results. Recent findings highlight that users can significantly improve answer quality by asking the model to "reason step by step." This approach, known as chain-of-thought prompting, has been widely adopted because it helps the AI break down complex tasks instead of making a leap and possibly an error. By structuring the analysis (much like IRAC or element-by-element examination), you not only get a thorough answer but can also verify each step of the reasoning. If the model makes a mistake in a step, you can catch it and correct it, resulting in a more reliable final answer. In legal reasoning, where analytical rigor is key, this method ensures the AI considers all necessary components (for example, each element of a claim or each prong of a test). It effectively guides the model to "think like a lawyer," aligning its process with how a legal professional would logically approach the issue. Even if newer LLMs can sometimes do this internally, explicitly prompting for step-by-step reasoning is a safe way to enforce completeness and clarity in the output.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique5_example_question = {
        'en': 'Assessing legal liability with multiple elements. (A customer slipped and fell in a store – does the store have negligence liability?)',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique5_example_bad_prompt = {
        'en': 'The customer slipped on a wet floor in the store and was injured. Is the store liable for negligence?',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique5_example_good_prompt = {
        'en': 'You are a legal analyst. Analyze the following scenario step by step to determine if the store could be held liable for negligence: A customer in a grocery store slipped on a spilled liquid and broke their arm. First, identify the elements required to prove negligence in U.S. law (duty, breach, causation, damages). Then, discuss each element one by one with respect to the facts (e.g., did the store owe a duty, did it breach that duty by not cleaning the spill, etc.). Conclude whether the elements are satisfied and thus if the store is likely liable.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique5_example_explanation = {
        'en': "This prompt explicitly asks for a step-by-step IRAC-style analysis. It not only tells the AI to consider each negligence element in order but also reminds it of what those elements are. The instruction ensures the answer will be organized (perhaps with headings or paragraphs for Duty, Breach, Causation, Damages, Conclusion). The model is less likely to omit a part of the analysis, and the user will get a structured explanation rather than a one-liner. By guiding the reasoning process, the prompt helps the AI reach a well-founded conclusion (or identify if information is missing) just as a human lawyer would.\n\nExample output: \"*Duty: The store, as a business open to the public, owes its customers a legal duty of care to maintain the premises in a reasonably safe condition. Here, that duty means regularly inspecting for hazards like spills and either cleaning them promptly or warning customers (e.g., with a 'Wet Floor' sign).\n\nBreach: We examine if the store breached its duty by failing to address the spilled liquid. If the spill was present long enough that employees should have noticed it (say, it had been on the floor for 30 minutes without cleanup), not cleaning it would likely be a breach of duty. If the spill happened moments before the fall, the store might argue it had no reasonable opportunity to discover and fix it, which could negate breach.\n\nCausation: The customer's injury must be caused by the store's breach. Here, the causal link is direct: the unsafe condition (wet floor) led to the slip-and-fall accident. We'd also consider proximate cause – it's foreseeable that an unaddressed spill leads to this kind of injury, so causation is established.\n\nDamages: The customer suffered actual harm (a broken arm, medical bills, etc.), satisfying the damages element required for negligence.\n\nConclusion: If evidence shows the spill was on the floor long enough that the store should have known and cleaned it, the store likely breached its duty. In that case, all four elements of negligence are met, and the store would likely be held liable for the customer's injury. If the spill was truly sudden and unforeseeable, the store might avoid liability, but absent such proof, this scenario points toward negligence on the store's part.*\"",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique5_resource_title = {'en': "Deloitte's Guide to Legal Prompting", 'pt': 'Placeholder for Portuguese translation'}
    technique5_resource_url = 'https://www2.deloitte.com/dl/en/pages/legal/articles/grundkurs-legal-prompting.html'
    technique5_resource_description = {
        'en': 'Comprehensive guide on effective legal prompting techniques including step-by-step reasoning',
        'pt': 'Placeholder for Portuguese translation',
    }
    return (
        technique5_description,
        technique5_example_bad_prompt,
        technique5_example_explanation,
        technique5_example_good_prompt,
        technique5_example_question,
        technique5_name,
        technique5_resource_description,
        technique5_resource_title,
        technique5_resource_url,
        technique5_slug,
        technique5_why_it_works,
    )


@app.cell(hide_code=True)
def _():
    technique6_slug = 'contract-extraction'
    technique6_name = {'en': 'Extracting Key Provisions and Data from Contracts', 'pt': 'Placeholder for Portuguese translation'}
    technique6_description = {
        'en': 'This technique involves directing an LLM to locate and extract specific information from legal documents like contracts, rather than summarizing the entire document. By focusing the model on particular provisions, clauses, or data points, attorneys can quickly find relevant information such as dates, obligations, defined terms, or conditions. The approach is similar to using targeted questions with a colleague who has read a document - except the LLM does the quick read-through and extraction for you.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique6_why_it_works = {
        'en': "Legal documents are often lengthy and complex, with critical details buried within dense paragraphs. By prompting the LLM to focus on specific provisions or information types, you eliminate the noise and zero in on what matters. This technique works because LLMs have strong pattern recognition abilities that can identify the relevant clauses or data points when properly directed. Rather than processing the entire document (which might exceed the model's context window anyway), a targeted extraction prompt creates efficiency by pulling only the needed information. This is particularly valuable when reviewing multiple agreements or when specific contractual elements (like termination rights, payment terms, or warranty provisions) need quick assessment across documents.",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique6_example_question = {
        'en': "Understanding a contract's liquidated damages provision. (You need to know how damages for breach are handled in a long agreement.)",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique6_example_bad_prompt = {
        'en': 'Tell me about this contract. [entire 50-page contract pasted]',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique6_example_good_prompt = {
        'en': "In the clause below, what do the parties agree regarding damages for breach?\n\n12.2 Liquidated Damages Not Penalty. Because of the unique nature of the economic damages that may be sustained by the Company in the event of a breach of certain provisions of this Agreement by Executive, it is acknowledged and agreed by the Parties that it would be impracticable and extremely difficult to ascertain with any degree of certainty the amount of damages which the Company would sustain as a result of such breach. Accordingly, if Executive breaches certain provisions of this Agreement, the Parties agree that any sums payable under this Agreement in such circumstances are in the nature of liquidated damages and not a penalty, and represent a reasonable estimate of the damages that the Company will suffer in the event of Executive's breach.\n\nSummarize the effect of this clause in bullet points, explaining what this means for both parties if there's a breach.",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique6_example_explanation = {
        'en': 'The good prompt does several things right: it isolates just the relevant clause (12.2) rather than sending the entire contract, asks a specific question about breach damages, and requests a structured response format (bullet points). This leads the LLM to focus solely on interpreting the liquidated damages provision, which establishes that certain payments for breach: 1) are considered liquidated damages not penalties, 2) are justified because actual damages would be difficult to measure, and 3) represent what the parties agree is a reasonable estimate of potential harm. The model doesn\'t waste time analyzing unrelated sections of the agreement, and the attorney gets precisely the information needed: the nature and justification of the damages provision. This extraction approach is significantly more efficient than asking for a general contract summary and then hunting through it for damage provisions.\n\nExample output: "• Effect of Clause 12.2 - Liquidated Damages:\n• The clause establishes that certain breach payments are classified as liquidated damages, not penalties\n• Both parties acknowledge that actual economic damages from specific breaches would be difficult to calculate with certainty\n• The payments represent a reasonable pre-estimate of potential damages, not punishment\n• This classification matters legally because courts generally enforce liquidated damages provisions but may invalidate penalty clauses\n• For the executive: limits potential argument that the damages are excessive or punitive\n• For the company: provides more certainty that the damage amounts will be enforceable if challenged in court"',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique6_resource_title = {'en': 'Ethylene Sales Agreement', 'pt': 'Placeholder for Portuguese translation'}
    technique6_resource_url = 'https://www.sec.gov/Archives/edgar/data/1604665/000119312514263367/d715499dex104.htm'
    technique6_resource_description = {
        'en': 'A complex and long agreement, perfect for this example.',
        'pt': 'Placeholder for Portuguese translation',
    }
    return (
        technique6_description,
        technique6_example_bad_prompt,
        technique6_example_explanation,
        technique6_example_good_prompt,
        technique6_example_question,
        technique6_name,
        technique6_resource_description,
        technique6_resource_title,
        technique6_resource_url,
        technique6_slug,
        technique6_why_it_works,
    )


@app.cell(hide_code=True)
def _():
    technique7_slug = 'msa-clause-drafting'
    technique7_name = {'en': 'Master Service Agreement Clause Drafting and Refinement'}
    technique7_description = {
        'en': 'This technique involves using LLMs to draft new clauses or refine existing language in Master Service Agreements (MSAs). By setting clear parameters about the purpose, required terms, governing law, and desired style, you can generate high-quality legal text that meets your specific needs. The model can either create clauses from scratch or suggest improvements to existing language, accelerating the drafting process while ensuring the output aligns with legal standards.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique7_why_it_works = {
        'en': "LLMs have been trained on vast repositories of legal documents, including agreements filed with the SEC. This training enables them to understand the structure, terminology, and conventional language of MSAs and other legal agreements. By providing specific context (jurisdiction, industry, desired complexity level) and parameters (required elements, formatting preferences), you narrow the model's focus to produce relevant, properly structured legal text. The model can quickly generate initial drafts that follow standard legal conventions or modernize outdated language, saving significant time compared to manual drafting. However, human review remains essential to ensure the output is legally sound and contextually appropriate for your specific transaction.",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique7_example_question = {
        'en': 'Drafting or refining confidentiality clauses in a Master Service Agreement. (You need to create or improve language around confidential information protection.)',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique7_example_bad_prompt = {'en': 'Write a confidentiality clause for my MSA.', 'pt': 'Placeholder for Portuguese translation'}
    technique7_example_good_prompt = {
        'en': 'You are a lawyer drafting a confidentiality clause for a Master Service Agreement between a technology vendor and healthcare client under California law. Reference the structure in the SEC filing at https://www.sec.gov/Archives/edgar/data/1042134/000119312505162630/dex1033.htm. The clause should cover: (1) definition of confidential information, (2) obligations to maintain secrecy, (3) standard exceptions (public information, independently developed information, etc.), (4) duration of obligations (3 years post-termination), and (5) return of confidential information upon termination. Write the clause in plain English while maintaining necessary legal protections. Format with numbered subsections for readability.',
        'pt': 'Placeholder for Portuguese translation',
    }
    technique7_example_explanation = {
        'en': "The good prompt provides extensive context and direction for creating an effective confidentiality clause. It specifies the type of agreement (MSA), the parties involved (tech vendor and healthcare client), the governing law (California), and references a specific SEC filing as a structural guide. The prompt also clearly outlines the five key elements that must be included in the clause and provides specific parameters (3-year post-termination duration). Furthermore, it guides the style ('plain English') and formatting ('numbered subsections'), ensuring the output will be both legally sound and reader-friendly.\n\nBy contrast, the bad prompt gives virtually no information about context, content requirements, style preferences, or formatting needs, which would likely result in a generic clause that might not address the specific needs of a technology-healthcare relationship or conform to California law. The specificity in the good prompt ensures the model produces a clause that closely matches what would appear in a professionally drafted MSA, with appropriate attention to healthcare data concerns and technology service specifics.\n\nThe resulting clause might begin with a definition section that carefully defines confidential information in the healthcare technology context, outline specific security measures required for protected health information, list standard exceptions to confidentiality obligations, specify the 3-year post-termination period, and detail the procedures for returning or destroying confidential information when the agreement ends.",
        'pt': 'Placeholder for Portuguese translation',
    }
    technique7_resource_title = {'en': 'Master Service Agreement', 'pt': 'Placeholder for Portuguese translation'}
    technique7_resource_url = 'https://www.sec.gov/Archives/edgar/data/1042134/000119312505162630/dex1033.htm'
    technique7_resource_description = {
        'en': 'A complex and long agreement, perfect for this example, but now techy.',
        'pt': 'Placeholder for Portuguese translation',
    }
    return (
        technique7_description,
        technique7_example_bad_prompt,
        technique7_example_explanation,
        technique7_example_good_prompt,
        technique7_example_question,
        technique7_name,
        technique7_resource_description,
        technique7_resource_title,
        technique7_resource_url,
        technique7_slug,
        technique7_why_it_works,
    )


@app.cell
def _(DirectLLMClient, mo):
    def display_response(user_prompt: str = None):
        """Create a nice Marimo UI element to display the prompt and response with a loading spinner."""
        if not user_prompt.value:
            return mo.md(
                f"""
                <div style="margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                    <div style="background-color: #f5f5f5; padding: 15px; border-bottom: 1px solid #ddd;">
                        <strong>Prompt:</strong>
                        <div style="margin-top: 8px; font-style: italic;">No prompt provided yet.</div>
                    </div>
                    <div style="padding: 15px;">
                        <strong>Response:</strong>
                        <div style="margin-top: 8px; white-space: pre-wrap;">We will have a response from the model here.</div>
                    </div>
                </div>
                """
            )

        client = DirectLLMClient(provider='openai')

        # Display a loading message with a spinner
        with mo.status.spinner(subtitle='Generating response...') as spinner:
            response = client.generate(prompt=user_prompt.value, system_message='You are a helpful assistant.')
            spinner.update(subtitle='Formatting response...')

        final_response = mo.vstack(
            [
                mo.md(
                    f"""
            <div style="margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden;">
                <div style="background-color: #f5f5f5; padding: 15px; border-bottom: 1px solid #ddd;">
                    <strong>Prompt:</strong>
                    <div style="margin-top: 8px; font-style: italic;">{user_prompt.value}</div>
                </div>
                <div style="padding: 15px;">
                    <strong>Response:</strong>
                </div>
            </div>
            """
                ),
                mo.md(response),
            ]
        )
        return final_response
    return (display_response,)


@app.cell(hide_code=True)
def _():
    # Cell: Define Technique 8
    technique8_slug = 'ambiguity-interpretation'
    technique8_name = {'en': 'Handling Ambiguity and Multiple Interpretations', 'pt': 'Lidando com Ambiguidade e Múltiplas Interpretações'}
    technique8_description = {
        'en': 'Legal language is notoriously prone to ambiguity. A well-designed prompt can help explore different interpretations of a clause or identify unclear wording. If you suspect a contract clause or statute could be read in more than one way, prompt the model to analyze it from multiple angles. This technique leverages the LLM to surface different possible readings of ambiguous text, helping lawyers anticipate potential disputes or identify areas needing clearer drafting.',
        'pt': 'A linguagem jurídica é notoriamente propensa à ambiguidade. Um prompt bem elaborado pode ajudar a explorar diferentes interpretações de uma cláusula ou identificar redação pouco clara. Se você suspeitar que uma cláusula contratual ou estatuto pode ser lido de mais de uma maneira, solicite ao modelo que o analise de múltiplos ângulos.',
    }
    technique8_why_it_works = {
        'en': 'Ambiguity in legal documents can lead to disputes and litigation. By explicitly asking an LLM to provide multiple interpretations of ambiguous language, you prevent the model from committing to a single answer and instead encourage it to explore all plausible readings. This is particularly valuable in cross-border or bilingual contracts where cultural and linguistic differences can create additional layers of ambiguity. For example, contracts between English and Chinese parties may have subtle but significant differences in translation that affect legal interpretation. The LLM can identify these potential discrepancies when properly prompted, allowing attorneys to anticipate arguments from both sides and draft clearer language. Since the model has been trained on vast legal corpora, it can recognize common patterns of ambiguity and suggest alternative readings that might not be immediately apparent, serving as a valuable thought partner in identifying potential issues before they become disputes.',
        'pt': 'A ambiguidade em documentos legais pode levar a disputas e litígios. Ao solicitar explicitamente que um LLM forneça múltiplas interpretações de linguagem ambígua, você impede que o modelo se comprometa com uma única resposta e, em vez disso, o incentiva a explorar todas as leituras plausíveis.',
    }
    technique8_example_question = {
        'en': 'Analyzing a potentially ambiguous non-compete clause in a contract. (The scope of prohibited activities is unclear.)',
        'pt': 'Analisando uma cláusula de não concorrência potencialmente ambígua em um contrato.',
    }
    technique8_example_bad_prompt = {
        'en': 'What does this non-compete clause mean: "Party A shall not engage in any business similar to Party B\'s business for two years in the same city"?',
        'pt': 'O que significa esta cláusula de não concorrência: "A Parte A não deve se envolver em nenhum negócio semelhante ao negócio da Parte B por dois anos na mesma cidade"?',
    }
    technique8_example_good_prompt = {
        'en': 'The following non-compete clause may be ambiguous: "Party A shall not engage in any business similar to Party B\'s business for two years in the same city." What are three different ways one could interpret the scope of "engage in any business" in this context? For each interpretation, explain: 1) What specific activities would be prohibited, 2) What activities might still be permitted, and 3) Which party would likely favor this interpretation. Then suggest a clearer rewriting that would eliminate the ambiguity.',
        'pt': 'A seguinte cláusula de não concorrência pode ser ambígua: "A Parte A não deve se envolver em nenhum negócio semelhante ao negócio da Parte B por dois anos na mesma cidade." Quais são três maneiras diferentes de interpretar o escopo de "se envolver em qualquer negócio" neste contexto?',
    }
    technique8_example_explanation = {
        'en': "The good prompt specifically identifies where the ambiguity lies ('engage in any business') and asks for multiple interpretations (three), with structured analysis of each. By requesting the model to explain which activities would be prohibited versus permitted under each reading, and which party would favor each interpretation, the prompt encourages a balanced, thorough analysis from different perspectives. The request for a clearer rewriting provides practical value beyond just identifying the problem. This approach transforms the LLM into a collaborative thought partner that helps anticipate potential arguments from both sides of a future dispute.\n\nExample output: \"Interpretation 1 (Broadest): 'Engage in any business' prohibits Party A from any involvement whatsoever with competing businesses, including: employment at any level, consulting work, passive investment (even minor shareholding), and of course founding or operating a competing business. Under this reading, Party A could still work in unrelated industries or in the same industry outside the specified city. Party B would favor this interpretation as it maximizes protection from competition.\n\nInterpretation 2 (Moderate): 'Engage in any business' means actively participating in the operation or management of a competing business, including: founding a competing company, serving as an executive or manager, or working in a significant capacity that leverages industry knowledge. Under this reading, Party A could still make passive investments or hold non-management positions in competing businesses. Neither party clearly benefits, as this represents a middle ground.\n\nInterpretation 3 (Narrowest): 'Engage in any business' refers only to founding, owning, or controlling a competing business. Under this reading, Party A would be prohibited from starting their own competing venture or being a controlling shareholder, but could freely work as an employee, consultant, or minor investor in competing businesses. Party A would favor this interpretation as it preserves most employment opportunities.\n\nClearer rewriting: 'For a period of two years following the Effective Date, Party A shall not, within the same city as Party B: (i) found, own, operate, or control any business that offers products or services similar to Party B's business; (ii) serve as an officer, director, or manager of any such business; (iii) provide consulting services to any such business; or (iv) own more than 5% equity interest in any such business. For clarity, employment in non-managerial positions with companies competing with Party B is not prohibited.'\"",
        'pt': "O bom prompt identifica especificamente onde reside a ambiguidade ('se envolver em qualquer negócio') e pede múltiplas interpretações (três), com análise estruturada de cada uma.",
    }
    technique8_resource_title = {
        'en': 'Using English-Language Contracts in China: My Q&A with China Law Blog',
        'pt': 'Usando Contratos em Inglês na China',
    }
    technique8_resource_url = 'https://www.adamsdrafting.com/using-english-language-contracts-in-china-my-q-and-a-with-china-law-blog/'
    technique8_resource_description = {
        'en': "Insights on cross-language contract interpretation challenges. Adam is just really good. If you ever read this, Adam, I'm your fan since 2011!",
        'pt': 'Insights sobre desafios de interpretação de contratos em diferentes idiomas. Adam é simplesmente ótimo. Se você algum dia ler isto, Adam, sou seu fã desde 2011!',
    }
    return (
        technique8_description,
        technique8_example_bad_prompt,
        technique8_example_explanation,
        technique8_example_good_prompt,
        technique8_example_question,
        technique8_name,
        technique8_resource_description,
        technique8_resource_title,
        technique8_resource_url,
        technique8_slug,
        technique8_why_it_works,
    )


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _():
    # Cell: Define Technique 9
    technique9_slug = 'comparative-law'
    technique9_name = {'en': 'Comparative Law Analysis Across Jurisdictions', 'pt': 'Análise Comparativa de Leis Entre Jurisdições'}
    technique9_description = {
        'en': 'Legal outcomes can vary dramatically across jurisdictions. A savvy prompt will recognize when a question requires a comparative approach and instruct the model to address each jurisdiction separately. This technique is useful for questions like, "How do the laws of the US and EU differ on data protection?" or "Compare patent eligibility in the US versus China." By explicitly naming the jurisdictions and requesting a structured comparison, you can obtain a clearer understanding of how different legal systems approach the same issue.',
        'pt': 'Os resultados legais podem variar dramaticamente entre jurisdições. Um prompt inteligente reconhece quando uma questão requer uma abordagem comparativa e instrui o modelo a abordar cada jurisdição separadamente. Esta técnica é útil para perguntas como, "Como as leis dos EUA e da UE diferem na proteção de dados?" ou "Compare a elegibilidade de patentes nos EUA versus China."',
    }
    technique9_why_it_works = {
        'en': 'Legal systems have fundamental differences in structure, principles, and priorities. Common law jurisdictions (like the US and UK) rely heavily on case precedent, while civil law systems (like Brazil and France) are grounded in comprehensive legal codes. When you explicitly name the jurisdictions and the specific legal issue at hand, you guide the model to access its knowledge about each distinct legal system rather than blending approaches. This technique acknowledges the reality of legal practice: that practitioners must consider the specific governing law of their case. Structured comparison also improves clarity, as the differences between jurisdictions become immediately apparent when presented side by side. Authoritative legal resources often present information in this comparative format precisely because it highlights key distinctions that might otherwise be lost in a generalized discussion.',
        'pt': 'Os sistemas jurídicos têm diferenças fundamentais em estrutura, princípios e prioridades. Jurisdições de common law (como EUA e Reino Unido) dependem fortemente de precedentes de casos, enquanto sistemas de direito civil (como Brasil e França) são fundamentados em códigos legais abrangentes. Ao nomear explicitamente as jurisdições e a questão jurídica específica, você orienta o modelo a acessar seu conhecimento sobre cada sistema jurídico distinto.',
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
        'pt': 'Compare como as cláusulas penais em contratos são tratadas segundo a lei de Nova York, a lei inglesa e a lei brasileira. Destaque as diferenças na aplicabilidade e quaisquer limitações legais em cada jurisdição.',
    }
    technique9_example_explanation = {
        'en': "The good prompt explicitly names three jurisdictions (New York, England, and Brazil) and the specific legal concept (penalty clauses in contracts). It also requests a structured format with the jurisdictions clearly separated. This approach will yield a response that helps the user understand exactly how each legal system handles penalty clauses, rather than receiving a vague, generalized answer that might not apply in their situation.\n\nThe model's response would likely be organized by jurisdiction with clear distinctions highlighted. For New York and English law (both common law systems), the model would explain the strong prohibition against penalty clauses while allowing legitimate liquidated damages. For Brazilian law (a civil law system), it would note the different approach where penalty clauses are recognized and enforceable but subject to statutory limitations. The structured format makes these critical differences immediately apparent.\n\nThis comparative approach is particularly valuable for transactional lawyers drafting agreements that might be enforced in multiple jurisdictions. Without this clear comparison, a lawyer might draft provisions that would be unenforceable in some of the relevant jurisdictions. The prompt's request for relevant legal principles or cases also helps ensure the response includes authoritative support for each jurisdiction's approach, making the answer more reliable and trustworthy.\n\nExample output might include:\n\n**New York Law**\n- Follows general common law principles - clauses deemed a \"penalty\" (punitive in nature) are not enforceable\n- Courts distinguish between unenforceable penalty clauses and enforceable liquidated damages clauses\n- Key test: Is the amount a reasonable pre-estimate of loss (enforceable) or punitive (unenforceable)?\n- Courts will assess if the amount is disproportionate to the actual harm\n\n**English Law**\n- Similar to New York, as the origin of the common law rule against penalties\n- Leading case: Dunlop Pneumatic Tyre Co. v. New Garage (1915) established tests to distinguish penalties from genuine liquidated damages\n- Modern development: Cavendish Square Holding v. Makdessi refined this test\n- Core principle: If a clause imposes a detriment out of proportion to any legitimate interest in enforcement, it's an unenforceable penalty\n\n**Brazilian Law**\n- Civil law approach differs significantly from common law jurisdictions\n- The concept of a \"penalty clause\" (cláusula penal) is recognized and enforceable, but regulated by statute\n- According to the Brazilian Civil Code, any contractual penalty cannot exceed the value of the main obligation\n- Courts can reduce the penalty if deemed excessive or if there's partial performance\n- Core difference: Brazil does not follow the common law penalty doctrine; it enforces agreed penalties within statutory limits",
        'pt': 'O bom prompt nomeia explicitamente três jurisdições (Nova York, Inglaterra e Brasil) e o conceito jurídico específico (cláusulas penais em contratos). Também solicita um formato estruturado com as jurisdições claramente separadas.',
    }
    technique9_resource_title = {'en': 'Brazil Civil Code 2018 Amendments', 'pt': 'Código Civil Brasileiro Emendas de 2018'}
    technique9_resource_url = 'https://webfiles-sc1.blackbaud.com/files/support/helpfiles/npoconnect-qa/content/resources/attachments/brazil-law-civil-code-13.777-2018.pdf'
    technique9_resource_description = {
        'en': "Reference document showing Brazil's civil law approach to contract provisions",
        'pt': 'Documento de referência mostrando a abordagem do direito civil brasileiro para provisões contratuais',
    }
    return (
        technique9_description,
        technique9_example_bad_prompt,
        technique9_example_explanation,
        technique9_example_good_prompt,
        technique9_example_question,
        technique9_name,
        technique9_resource_description,
        technique9_resource_title,
        technique9_resource_url,
        technique9_slug,
        technique9_why_it_works,
    )


@app.cell(hide_code=True)
def _(get_current_language, mo, translations):
    def create_enhanced_interactive_playground(
        technique_name,
        bad_prompt,
        good_prompt,
    ):
        """
        Creates an interactive playground structure (without form values)
        """
        # Create the playground header
        playground_header = mo.md(f"""
        <div style="background-color: #f0f4f8; padding: 20px 40px 20px 40px; border-left: 5px solid #4a5568; margin-bottom: 10px; font-family: 'Garamond', serif;">
            <h3 style="color: #000000; margin-top: 0; margin-bottom: 10px; font-size: 1.2em; font-weight: 400; text-align: left; font-family: 'Garamond', serif;">
                Try it yourself!

                {translations['chat_experiment'][get_current_language()]} - Technique: <span style="color: #3182ce; font-weight: bold;">{technique_name[get_current_language()]}</span>
            </h3>
        </div>
        """)

        # Return components to be used by other cells
        return {'technique_name': technique_name, 'bad_prompt': bad_prompt, 'good_prompt': good_prompt, 'header': playground_header}
    return (create_enhanced_interactive_playground,)


@app.cell
def _(mo):
    def generate_output(form, examples):
        """Generate output based on form submission or examples selection"""
        if form.value is not None:
            return mo.vstack(
                [
                    mo.md(
                        f"""
                        <div style="font-family: Garamond, serif; border: 2px solid #ccc; border-radius: 5px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <h3>Select an option to view its content.</h3>
                            <pre style="white-space: pre-wrap; word-wrap: break-word;">{form.value}</pre>
                            <p><em>(Results will be available on the next page)</em></p>
                        </div>
                        """
                    ),
                ]
            )
        else:
            return mo.vstack(
                [
                    mo.md(
                        f"""
                        <div style="font-family: Garamond, serif; border: 2px solid #ccc; border-radius: 5px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                            <h3>Current Selection:</h3>
                            <pre style="white-space: pre-wrap; word-wrap: break-word;">{examples.value.get('prompt', '')}</pre>
                            <p><em>(Results will be available on the next page)</em></p>
                        </div>
                        """
                    ),
                ]
            )
    return (generate_output,)


@app.cell
def _(get_current_language, mo, translations):
    def generate_form(examples):
        """Generate form based on examples dropdown"""
        return mo.ui.text_area(
            label=translations['your_prompt'][get_current_language()],
            placeholder=translations['enter_prompt_here'][get_current_language()],
            value=examples.value.get('prompt', ''),
            full_width=True,
            rows=5,
        ).form(
            submit_button_label=translations['send_prompt'][get_current_language()], bordered=True, clear_on_submit=True, show_clear_button=True
        )
    return (generate_form,)


@app.cell(hide_code=True)
def ch_1():
    technique10_slug = 'le-gran-finale'
    technique10_name = {
        'en': 'Le Gran Finalle: How do I use it and why you should too (or recency bias)',
        'pt': 'Le Gran Finale: O Efeito de Recência',
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
        'pt': 'Como posso redigir um melhor memorando de pesquisa jurídica?',
    }

    technique10_example_bad_prompt = {
        'en': '[After spending hours providing detailed, relevant, snippets of the brief, everything that a human would love to have, but disorganized background information on fair use law.] I need a legal research memo on fair use exceptions. Include relevant case law, persuasive arguments, and structure it properly with Bluebook citations.',
        'pt': 'Preciso de ajuda para escrever um memorando de pesquisa jurídica sobre exceções de uso justo em direitos autorais. Por favor, torne-o persuasivo, estruturado, citando jurisprudência relevante e com formatação adequada para um escritório de advocacia.',
    }

    technique10_example_good_prompt = {
        'en': "[After resetting the conversation and providing only Campbell v. Acuff-Rose Music as context.] Draft a legal research memo analyzing whether a university professor showing 10-minute clips from mainstream films in class qualifies as fair use.\n\nHERE'S WHAT MATTERS MOST (I TIODL INE MLLION TIKMES IT NEEDS THE FOIRKM ATT!!!!!111!!):\n\n1. USE THE STANDARD MEMO STRUCUTRE (FACTS, ISSUE, SHORT ANSWER, ANALYSIS, CONCLUSION).\n2. CITE RELEVANT CASE LAW INCLUDING CAMPBELL V. ACUFF-ROSE MUSIC\n3. FULLY ANALYZE ALL FOUR FAIR USE FACTORS\n4. USE BLUEBOOK CITATION FORMAT!!!111!!\n5. CLEARLY STATE A STRONG RECOMMENDATION IN THE CONCLUSOIN. AGASUIFN BLKUEBOOK!!! IM NOT A FFFWW JOURNaLTTis!!11!",
        'pt': 'Preciso de ajuda para escrever um memorando de pesquisa jurídica sobre exceções de uso justo em direitos autorais. O memorando deve analisar se um professor universitário que mostra clipes de 10 minutos de filmes mainstream em uma aula de estudos cinematográficos se qualificaria como uso justo.\n\nAQUI ESTÁ O QUE MAIS IMPORTA:\n\n1. Siga o formato IRAC (Questão, Regra, Análise, Conclusão)\n2. Cite jurisprudência relevante, incluindo Campbell v. Acuff-Rose Music\n3. Analise profundamente os quatro fatores do uso justo\n4. Formate o memorando com citação jurídica adequada no estilo Bluebook\n5. Inclua uma recomendação clara na seção de conclusão',
    }
    technique10_example_explanation = {
        'en': 'The ineffective prompt buries key instructions within scattered context. The effective prompt clearly emphasizes critical instructions at the end, including intentional capitalization and typing mistakes, capitalizing on the model’s natural recency bias to maximize compliance.',
        'pt': 'O prompt ineficaz mistura todos os requisitos sem ênfase. O prompt eficaz coloca instruções específicas no final em uma lista numerada visualmente distinta—exatamente onde a atenção do modelo é mais forte. Ao enfatizar os requisitos críticos com letras maiúsculas e posicioná-los no final, aumentamos drasticamente a probabilidade de execução fiel.',
    }

    technique10_resource_title = {
        'en': 'Lost in the Middle: How Language Models Use Long Contexts',
        'pt': 'O Efeito de Posição em Modelos de Linguagem',
    }
    technique10_resource_url = {'https://arxiv.org/abs/2307.03172'}
    technique10_resource_description = {
        'en': 'This paper from UC Berkeley researchers explores how information positioning within prompts affects language model responses, particularly highlighting the recency effect.',
        'pt': 'Este artigo acadêmico de pesquisadores da UC Berkeley examina como a posição das informações dentro de um prompt afeta significativamente a resposta de um modelo de linguagem, com atenção especial ao fenômeno do efeito de recência.',
    }
    return (
        technique10_description,
        technique10_example_bad_prompt,
        technique10_example_explanation,
        technique10_example_good_prompt,
        technique10_example_question,
        technique10_name,
        technique10_resource_description,
        technique10_resource_title,
        technique10_resource_url,
        technique10_slug,
        technique10_why_it_works,
    )


@app.cell(hide_code=True)
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
            playground_data['bad_prompt'][get_current_language()], playground_data['good_prompt'][get_current_language()]
        )

        # Return data needed for the next cell
        return playground_data['header'], examples
    return (create_interactive_playground_number,)


@app.cell(hide_code=True)
def _(get_current_language, mo, translations):
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
        <div class="technique-header" style="background-color: #f0f4f8; padding: 40px 40px 0 40px; border-left: 5px solid #4a5568; margin-bottom: 0px; font-family: 'Garamond', serif; width: 100%; box-sizing: border-box;">
            <h2 style="color: #000000; margin-top: 0; margin-bottom: 2.5px; font-size: 1.3em; font-weight: 400; text-align: left; font-family: 'Garamond', serif;">{technique_name[get_current_language()]}</h2>
            <p style="font-size: 1em; padding-top: 10px; margin: 0; color: #000000; font-weight: 200; text-align: left; padding-bottom: 15px; font-family: 'Garamond', serif;">{technique_description[get_current_language()]}</p>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0)); margin: 10px 0 20px 0;">
                <h3 style="color: #000000; padding-bottom: 20px; font-size: 1.2em; margin: 0; font-weight: 400; text-align: center; font-family: 'Garamond', serif;">
                {translations['issue'][get_current_language()]}: {technique_example_question[get_current_language()]}
            </h3>
        </div>
        """)
        example_tabs = mo.ui.tabs(
            {
                translations['without_technique'][get_current_language()]: mo.md(f"""
                <div class="technique-bad-example" style="background-color: #fffbeb; padding: 15px; border-radius: 8px; border: 1px solid #f0c419; font-family: 'Garamond', serif;">
                    <h4 style="color: #8c7000; margin-top: 0; font-family: 'Garamond', serif;">{translations['without_technique'][get_current_language()]}</h4>
                    <div style="background-color: #fffbeb; padding: 10px; border-radius: 4px; border: 1px solid #fffbeb; font-family: 'Garamond', serif;">
                        <p style="font-family: 'Garamond', serif;">{technique_example_bad_prompt[get_current_language()]}</p>
                    </div>
                </div>
                """),
                translations['with_technique'][get_current_language()]: mo.md(f"""
                <div class="technique-good-example" style="background-color: #f8fdf7; padding: 15px; border-radius: 8px; border: 1px solid #4caf50; font-family: 'Garamond', serif;">
                    <h4 style="color: #2d6a30; margin-top: 0; font-family: 'Garamond', serif;">{translations['with_technique'][get_current_language()]}</h4>
                    <div style="background-color: #f8fdf7; padding: 10px; border-radius: 4px; border: 1px solid #f8fdf7; font-family: 'Garamond', serif;">
                        <p style="font-family: 'Garamond', serif;">{technique_example_good_prompt[get_current_language()]}</p>
                    </div>
                </div>
                """),
                translations['explanation'][get_current_language()]: mo.md(f"""
                <div class="technique-explanation" style="background-color: #fff0f0; padding: 15px; border-radius: 8px; border: 2px solid #b30000; font-family: 'Garamond', serif;">
        <h4 style="color: #2c5e8a; margin-top: 0; font-family: 'Garamond', serif;">{translations['explanation'][get_current_language()]}</h4>
        <p style="font-family: 'Garamond', serif;">{technique_example_explanation[get_current_language()]}</p>
    </div>
                """),
            }
        )

        why_it_works_accordion = mo.accordion(
            {
                translations['why_it_works'][get_current_language()]: mo.md(f"""
                <div class="technique-why-it-works" style="padding: 15px; background-color: #fff0f0; border-radius: 8px; font-family: 'Garamond', serif;">
                    <p style="color: #000000; font-family: 'Garamond', serif;">{technique_why_it_works[get_current_language()]}</p>
                </div>
                """)
            }
        )

        # Add more_resources accordion
        more_resources_accordion = mo.accordion(
            {
                'More Resources': mo.md(f"""
                <div class="technique-resources" style="padding: 15px; background-color: #fff0f0; border-radius: 8px; font-family: 'Garamond', serif;">
                    <p style="color: #000000; font-family: 'Garamond', serif;">{technique_resource_description[get_current_language()]}</p>
                    <br>
                    <a href="{technique_resource_url}" target="_blank" style="color: #0000FF; font-family: 'Garamond', serif;">{technique_resource_title[get_current_language()]}</a>
                    <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0)); margin: 10px 0 0 0;">
                </div>
                """)
            }
        )
        components = [technique_header, example_tabs, why_it_works_accordion, more_resources_accordion]

        return mo.vstack(components)
    return (display_technique_,)


@app.cell(hide_code=True)
def _(display_technique_):
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


@app.cell(hide_code=True)
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


@app.cell(hide_code=True)
def _(display_technique_number):
    # Display technique #2
    display_technique_number(2)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    display_technique_number(3)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    display_technique_number(4)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    display_technique_number(5)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    # Display technique #6
    display_technique_number(6)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    display_technique_number(7)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    display_technique_number(8)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    display_technique_number(9)
    return


@app.cell
def _():
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


@app.cell(hide_code=True)
def _(display_technique_number):
    display_technique_number(10)
    return


@app.cell
def _():
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
    mo.vstack([header10, examples10, form10, output10], justify='space-between', heights=[1, 2, 1, 1])
    return


@app.cell
def _(display_response, form10):
    # Display response for technique #10
    display_response(form10)
    return


@app.cell(hide_code=True)
def _():
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        <div style="display: flex; align-items: center; margin-bottom: 0px; padding: 50px 20px 0px 40px; background-color: #f0f4f8; border-left: 5px solid #4a5568; width: 100%; box-sizing: border-box; font-family: 'EB Garamond', 'Garamond', serif;">
            <div style="width: 100%;">
                <h1 style="margin: 0; color: #000000; text-align: left; font-weight: 400;">Thank you!</h1>
            </div>
        </div>

        <div style="padding: 30px 20px 0px 40px; background-color: #f0f4f8; margin-top: 0; font-family: 'Garamond', serif; border-left: 5px solid #4a5568;">
            <p>If you found errors or have any suggestions, please <a href="mailto:arthrod@umich.edu">let me know</a>.</p>

            <p style="margin-top: 20px;">Best,<br>Arthur</p>
        </div>
        """
    )
    return


if __name__ == "__main__":
    app.run()
