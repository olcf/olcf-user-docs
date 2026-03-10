======================================
OLCF Inference Service Documentation
======================================

.. note::

    All elements of the OLCF Inference service are in an
    **early release** state and are subject to change without notification.
    As such these resources should only be used for the purposes of testing
    and should not be relied upon for any production workflows.


.. important::
    Currently, the OLCF Inference Service is in a preview state and is currently only available by invitation

Welcome to the documentation for the OLCF Inference Service. This service provides access to powerful Large Language Models (LLMs) running on a highly optimized **vLLM runtime**, offering OpenAI-compatible API endpoints.

Authentication
--------------

To use the inference service, you must authenticate your requests using a Bearer token.

1. **Mint your token:** Tokens must be minted via myOLCF. More information can be found here :ref:`s3m_generate_token`
2. **Set your environment variable:** Once you have your token, we recommend exporting it securely in your terminal environment to prevent hardcoding it in your scripts.

.. code-block:: bash

   export S3M_TOKEN="your_minted_token_here"

Endpoint URL
------------

The primary base endpoint for chat completions is:

``https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/chat/completions``

Available Models
----------------

Currently, the service supports the following models:

* ``gpt-oss-120b``
* ``nemotron-nano-fp8``

Usage Examples (cURL)
---------------------

.. note::
    When using cURL, wget, or other command line programs please follow the best practices described in the S3M documentation :ref:`s3m_command_line_safety`

    You can follow the examples below by simply running

    .. code-block:: bash

        echo "Authorization: ${S3M_TOKEN}" > .env
        echo ".env" >> .gitignore

Because the service uses a vLLM backend, the request body is compatible with the standard OpenAI Chat Completions API format.

**Example 1: Querying gpt-oss-120b**

.. code-block:: bash

   curl -N -s -X POST "https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/chat/completions" \
        -H @.env \
        -H "Content-Type: application/json" \
        -d '{
              "model": "gpt-oss-120b",
              "messages": [{"role": "user", "content": "Your prompt here."}],
              "stream": false
            }'

**Example 2: Querying nemotron-nano-fp8**

.. code-block:: bash

   curl -N -s -X POST "https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/chat/completions" \
        -H @.env \
        -H "Content-Type: application/json" \
        -d '{
              "model": "nemotron-nano-fp8",
              "messages": [{"role": "user", "content": "Your prompt here."}],
              "stream": false
            }'

Python Usage (OpenAI Client)
----------------------------

Since the API is OpenAI-compatible, you can easily use the standard Python ``openai`` library. Simply override the base URL and pass your token.

.. code-block:: python

   from openai import OpenAI
   import os

   client = OpenAI(
       base_url="https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference",
       api_key=os.environ.get("S3M_TOKEN")
   )

   response = client.chat.completions.create(
       model="gpt-oss-120b",
       messages=[
           {"role": "user", "content": "Explain quantum computing in one sentence."}
       ],
       stream=False
   )

   print(response.choices[0].message.content)

Core API Endpoints
------------------

Because the service uses a vLLM backend, the API routing and request bodies are compatible with standard OpenAI API formats.

1. Chat Completions
^^^^^^^^^^^^^^^^^^^

**Endpoint:** ``/chat/completions``

Used for conversational interactions and instruction-following models.

.. code-block:: bash

   curl -N -s -X POST "https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/chat/completions" \
        -H @.env \
        -H "Content-Type: application/json" \
        -d '{
              "model": "gpt-oss-120b",
              "messages": [{"role": "user", "content": "Explain quantum computing."}],
              "stream": false
            }'

2. Standard Completions
^^^^^^^^^^^^^^^^^^^^^^^

**Endpoint:** ``/completions``

Used for traditional text continuation (base models rather than instruction-tuned chat models).

.. code-block:: bash

   curl -N -s -X POST "https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/completions" \
        -H @.env \
        -H "Content-Type: application/json" \
        -d '{
              "model": "nemotron-nano-fp8",
              "prompt": "The future of high-performance computing is",
              "max_tokens": 50,
              "temperature": 0.7
            }'

3. List Models
^^^^^^^^^^^^^^

**Endpoint:** ``/model/info``

If you need deeper configuration specs—such as maximum context length, supported modalities (e.g., vision/audio), or max output tokens—LiteLLM exposes a custom ``/model/info`` endpoint.

.. important::

    Because ``/model/info`` is a custom LiteLLM proxy route rather than a standard OpenAI route, you will use the standard Python ``requests`` library to fetch this data instead of the OpenAI SDK.

.. tab-set::

    .. tab-item:: **REST API (cURL):**

        .. code-block:: bash

           curl -s -X GET "https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/model/info" \
                -H @.env

    .. tab-item:: **Python (Requests Library):**

        .. code-block:: python

           import os
           import requests

           url = "https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/model/info"
           headers = {
               "Authorization": f"Bearer {os.environ.get('S3M_TOKEN')}"
           }

           response = requests.get(url, headers=headers)

           if response.status_code == 200:
               specs = response.json()
               for model in specs.get("data", []):
                   name = model.get("model_name")
                   info = model.get("model_info", {})
                   print(f"Model: {name}")
                   print(f"  - Max Input Tokens: {info.get('max_input_tokens', 'Unknown')}")
                   print(f"  - Max Output Tokens: {info.get('max_tokens', 'Unknown')}\n")
           else:
               print(f"Failed to fetch specs: {response.status_code}")


**Expected JSON Response:**

This will return a richer JSON payload containing the backend parameters and capabilities for each model on the server.

.. code-block:: json

   {
     "data": [
       {
         "model_name": "gpt-oss-120b",
         "litellm_params": {
           "model": "vllm/gpt-oss-120b"
         },
         "model_info": {
           "max_tokens": 8192,
           "max_input_tokens": 128000,
           "mode": "chat"
         }
       },
       {
         "model_name": "nemotron-nano-fp8",
         "litellm_params": {
           "model": "vllm/nemotron-nano-fp8"
         },
         "model_info": {
           "max_tokens": 4096,
           "max_input_tokens": 32768,
           "mode": "chat"
         }
       }
     ]
   }

4. Embeddings
^^^^^^^^^^^^^

**Endpoint:** ``/embeddings``

Generates vector embeddings for a given text. *(Note: Requires an embedding-specific model to be loaded on the server).*

.. code-block:: bash

   curl -s -X POST "https://testing.s3m.olcf.ornl.gov/olcf/open/v1alpha/inference/embeddings" \
        -H @.env \
        -H "Content-Type: application/json" \
        -d '{
              "model": "your-embedding-model-name",
              "input": "Text to vectorize."
            }'