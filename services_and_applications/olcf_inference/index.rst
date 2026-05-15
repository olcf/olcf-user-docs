======================================
OLCF Inference Service Documentation
======================================

Welcome to the documentation for the OLCF Inference Service.
This service flexes the :doc:`Secure Scientific Service Mesh (S3M) </services_and_applications/s3m/overview>` to provide access to powerful Large Language Models (LLMs) running on a highly optimized **vLLM runtime**, offering OpenAI-compatible API endpoints.


Requesting OLCF Inference Service Access
----------------------------------------

Please email OLCF Support `help@olcf.ornl.gov <mailto:help@olcf.ornl.gov>`__ if you are interested in using the OLCF Inference Service.

**Include the following information in your email:**
    * Existing OLCF Project ID
    * Project PI
    * Your project's use case - Please explain how your project will use the OLCF inference service in your workflow.


Authentication
--------------

To use the inference service, you must authenticate your requests using a Bearer token.

1. **Mint your token:** Tokens must be minted via :doc:`S3M </services_and_applications/s3m/overview>` on myOLCF. More information can be found in the :ref:`S3M documentation here <s3m_generate_token>`.
2. **Set your environment variable:** Once you have your token, we recommend exporting it securely in your terminal environment to prevent hardcoding it in your scripts.

.. code-block:: bash

   export S3M_TOKEN="your_minted_token_here"

Endpoint URL
------------

The primary base endpoint for chat completions is:

``https://s3m.olcf.ornl.gov/olcf/open/v1/inference/chat/completions``

.. _available_models:

Available Models
----------------

.. note::
    This list is not exhaustive. To see a complete list, please see :ref:`info_endpoint`

Currently, the service supports the following models:

.. list-table:: Supported Models
    :widths: 25 25 25
    :header-rows: 1

    * - Model
      - Aliases
      - Features
    * - `gpt-oss-120b <https://huggingface.co/openai/gpt-oss-120b>`__
      - ``gpt-oss-120b``, ``gpt-oss``
      - Text, Reasoning
    * - `nemotron-nano-fp8 <https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-FP8>`__
      - ``nemotron-nano-fp8``, ``nemotron-nano``
      - Text, Reasoning
    * - `apriel-1.6-15b-thinker <https://huggingface.co/ServiceNow-AI/Apriel-1.6-15b-Thinker>`__
      - ``apriel-1.6-15b-thinker``, ``apriel-15b-thinker``
      - Text, Reasoning, Vision
    * - `nomic-embed-text-v2-moe <https://huggingface.co/nomic-ai/nomic-embed-text-v2-moe>`__
      - ``nomic-embed-text-v2-moe``, ``nomic-embed-v2``
      - Text Embedding

Multi-Modal Inputs
------------------

For a working multimodal example, you can refer to :ref:`computer_vision`

For additional multimodal examples please see https://docs.vllm.ai/en/stable/features/multimodal_inputs/?h=multimodal#online-serving

OpenAI's file uploads are not supported on OLCF Inference Service, and the Service will not accept URL data pointing to web addresses.


Usage Examples
--------------

.. tab-set::

    .. tab-item:: cURL
        :sync: curl

        .. note::

            When using cURL, wget, or other command line programs please follow the best practices described in the S3M documentation :ref:`s3m_command_line_safety`

            You can follow the examples below by simply running

            .. code-block:: bash

                echo "Authorization: ${S3M_TOKEN}" > .env
                echo ".env" >> .gitignore

        Because the service uses a vLLM backend, the request body is compatible with the standard OpenAI Chat Completions API format.

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. note::

            In order to use the OpenAI Python library, you must first install it or activate an envrionment with it installed.
            You can install via pip with ``pip install openai``

        Since the API is OpenAI-compatible, you can easily use the standard Python ``openai`` library. Simply override the base URL and pass your token.


Querying gpt-oss-120b
^^^^^^^^^^^^^^^^^^^^^

.. tab-set::

    .. tab-item:: cURL
        :sync: curl

        .. code-block:: bash

           curl -N -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/chat/completions" \
                -H @.env \
                -H "Content-Type: application/json" \
                -d '{
                        "model": "gpt-oss-120b",
                        "messages": [
                            {"role": "user", "content": "Your prompt here."},
                            {"role": "user", "content": "We can be 120b(s)."}
                        ],
                        "stream": false
                    }'

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            from openai import OpenAI
            import os

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[
                    {"role": "user", "content": "Your prompt here"},
                    {"role": "user", "content": "We can be 120b(s)."}
                ],
                stream=False
            )

            print(response.choices[0].message.content)

Querying nemotron-nano-fp8
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. tab-set::

    .. tab-item:: cURL
        :sync: curl

        .. code-block:: bash

           curl -N -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/chat/completions" \
                -H @.env \
                -H "Content-Type: application/json" \
                -d '{
                      "model": "nemotron-nano-fp8",
                      "messages": [{"role": "user", "content": "Your prompt here."}],
                      "stream": false
                    }'

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            from openai import OpenAI
            import os

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            response = client.chat.completions.create(
                model="nemotron-nano-fp8",
                messages=[
                    {"role": "user", "content": "Your prompt here"}
                ],
                stream=False
            )

            print(response.choices[0].message.content)


.. _computer_vision:

Computer Vision
^^^^^^^^^^^^^^^

.. note::

    Computer vision is not supported by every model. Please see :ref:`available_models` and :ref:`info_endpoint` for details on which models support vision.

.. tab-set::
    .. tab-item:: cURL
        :sync: curl

        .. code-block:: bash

            jq -n --arg content "$(base64 < frontier.jpg)" '{
              "model": "apriel-1.6-15b-thinker",
              "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe the image."},
                        {
                            "type": "image_url",
                            "image_url": {"url": ("data:image/jpeg;base64," + $content)}
                        }
                    ]
                }
              ]
            }' | curl -N -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/chat/completions" \
                 -H @.env \
                 -H "Content-Type: application/json" \
                 -d @-

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            import base64
            import os
            from openai import OpenAI

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            # Function to encode the image
            def encode_image(image_path):
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")


            # Path to your image
            image_path = "frontier.jpg"

            # Getting the Base64 string
            base64_image = encode_image(image_path)

            response = client.chat.completions.create(
                model="apriel-1.6-15b-thinker",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "text", "text": "Describe the image." },
                            {
                                "type": "image_url",
                                "image_url": { "url": f"data:image/jpeg;base64,{base64_image}" },
                            },
                        ],
                    },
                ],
            )

            print(response.choices[0].message.content)

    .. tab-item:: Python (OpenAI - Responses)

        .. code-block:: python

            import base64
            import os
            from openai import OpenAI

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            # Function to encode the image
            def encode_image(image_path):
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode("utf-8")


            # Path to your image
            image_path = "frontier.jpg"

            # Getting the Base64 string
            base64_image = encode_image(image_path)

            response = client.responses.create(
                model="apriel-1.6-15b-thinker",
                input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": "Describe the image." },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        ],
                    },
                ],
            )

            print(response.output[0].content[0].text)


Simple Text Files
^^^^^^^^^^^^^^^^^

The ``file`` data type is not currently supported by any models on the OLCF Inference Service.
You will need to send the full text file as a ``string`` of long context to the service.

.. tab-set::

    .. tab-item:: cURL
        :sync: curl

        .. code-block:: bash

            jq -n --arg content "$(< <your simple text file>)" '{
                "model": "gpt-oss-120b",
                "messages": [
                    {
                        "role": "user",
                        "content": ("Process this text.\n\n" + $content)
                    }
                ]
            }' | curl -N -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/chat/completions" \
                 -H @.env \
                 -H "Content-Type: application/json" \
                 -d @-

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            from openai import OpenAI
            import os

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )


            with open("<your simple text file>", "rb") as f:
                data = f.read()

            response = client.chat.completions.create(
                model="nemotron-nano-fp8",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Process this text."
                            },
                            {
                                "type": "text",
                                "text": f"{data}"
                            },
                        ],
                    },
                ],
                stream=False
            )

            print(response.choices[0].message.content)


Core API Endpoints
------------------

Because the service uses a vLLM backend, the API routing and request bodies are compatible with standard OpenAI API formats.

**The API has a base URL located at: ``https://s3m.olcf.ornl.gov/olcf/open/v1/inference``**

Chat Completions
^^^^^^^^^^^^^^^^

**Endpoint:** ``/chat/completions``

Used for conversational interactions and instruction-following models.

.. tab-set::

    .. tab-item:: **REST API (cURL):**
        :sync: curl

        .. code-block:: bash

           curl -N -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/chat/completions" \
                -H @.env \
                -H "Content-Type: application/json" \
                -d '{
                      "model": "gpt-oss-120b",
                      "messages": [{"role": "user", "content": "Explain quantum computing."}],
                      "stream": false
                    }'

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            from openai import OpenAI
            import os

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            response = client.chat.completions.create(
                model="gpt-oss-120b",
                messages=[
                    {"role": "user", "content": "When was the first straw hat made?"}
                ],
                stream=False
            )

            # Access with:
            #response.choices[0].message.content


Standard Completions
^^^^^^^^^^^^^^^^^^^^

**Endpoint:** ``/completions``

Used for traditional text continuation (base models rather than instruction-tuned chat models).

.. tab-set::

    .. tab-item:: **REST API (cURL):**
        :sync: curl

        .. code-block:: bash

            curl -N -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/completions" \
                -H @.env \
                -H "Content-Type: application/json" \
                -d '{
                      "model": "nemotron-nano-fp8",
                      "prompt": "The future of high-performance computing is",
                      "max_tokens": 50,
                      "temperature": 0.7
                    }'

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            from openai import OpenAI
            import os

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            response = client.completions.create(
                model="gpt-oss-120b",
                prompt="You see, you're not dealing with the average AI user anymore..."
            )

            # Access with:
            #response.choices[0].text

.. _info_endpoint:

List Models
^^^^^^^^^^^

**Endpoint:** ``/models``

To view a list of available models use the ``/models`` endpoint.

.. tab-set::

    .. tab-item:: **REST API (cURL):**
        :sync: curl

        .. code-block:: bash

           curl -s -X GET "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/models" \
                -H @.env

    .. tab-item:: **Python (Requests Library):**
        :sync: requests

        .. code-block:: python

           import os
           import requests

           url = "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/models"
           headers = {
               "Authorization": f"Bearer {os.environ.get('S3M_TOKEN')}"
           }

           response = requests.get(url, headers=headers)

           if response.status_code == 200:
               specs = response.json()
               for model in specs.get("data", []):
                   name = model.get("id")
                   print(f"Model: {name}")
           else:
               print(f"Failed to fetch specs: {response.status_code}")

**Expected JSON Response:**

.. code-block:: json
    :force:

    {
        "data": [
            {
                "id": "nemotron-nano-fp8",
                "object": "model",
                "created": 1677610602,
                "owned_by": "openai"
            },
            {
                "id": "gpt-oss-120b",
                "object": "model",
                "created": 1677610602,
                "owned_by": "openai"
            },
            ...,
            ...
        ]
    }

Embeddings
^^^^^^^^^^

**Endpoint:** ``/embeddings``

Generates vector embeddings for a given text.

.. note::

    Embeddings require the use of an embedding-specific model. Check :ref:`available_models` and :ref:`info_endpoint` for embedding models.


.. tab-set::

    .. tab-item:: **REST API (cURL):**
        :sync: curl

        .. code-block:: bash

            curl -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/embeddings" \
                -H @.env \
                -H "Content-Type: application/json" \
                -d '{
                      "model": "nomic-embed-text-v2-moe",
                      "input": "This is good news."
                    }'


    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            import os
            from openai import OpenAI

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            embed_response = client.embeddings.create(
                model="nomic-embed-text-v2-moe",
                input="Are you sure?",
                encoding_format="base64",
            )

            # Access with:
            # embed_response.data[0].embedding

Responses
^^^^^^^^^

**Endpoint:** ``/responses``

A newer OpenAI API endpoint. Includes performance benefits and some additional features over chat completions.

Read more on OpenAI's Docs: https://developers.openai.com/api/docs/guides/migrate-to-responses

.. tab-set::

    .. tab-item:: **REST API (cURL):**
        :sync: curl

        .. code-block:: bash

            curl -s -X POST "https://s3m.olcf.ornl.gov/olcf/open/v1/inference/responses" \
                -H @.env \
                -H "Content-Type: application/json" \
                -d '{
                "model": "gpt-oss-120b",
                    "input": [
                        {
                             "role": "user",
                             "content": [
                                  { "type": "input_text", "text": "What is an AI agent?" },
                                  { "type": "input_text", "text": "Which agentic framework should I use for gpt-oss-120b?" }
                             ]
                        }
                    ]
                }'

    .. tab-item:: Python (OpenAI)
        :sync: openai

        .. code-block:: python

            import os
            from openai import OpenAI

            client = OpenAI(
                base_url="https://s3m.olcf.ornl.gov/olcf/open/v1/inference",
                api_key=os.environ.get("S3M_TOKEN")
            )

            response = client.responses.create(
                model="gpt-oss-120b",
                input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": "I'm using Python. Believe it!" },
                        ],
                    },
                ],
            )

            # Access with:
            #response.output[0].content[0].text


Additional Resources
--------------------

You can refer to both vLLM's API reference and OpenAI's API reference documentation for additional examples and instructions.

vLLM: https://docs.vllm.ai/en/stable/serving/openai_compatible_server/

OpenAI Chat Completions: https://developers.openai.com/api/reference/chat-completions/overview
