from setuptools import find_packages, setup

setup(
        name="stable_openai",
        version="0.1.1",
        author="Jellow",
        author_email="dvdx@foxmail.com",
        description="StableOpenai is an enhanced framework for OpenAI, providing stable and efficient API request "
                    "management. It allows the use of multiple API keys to increase request limits and ensures thread "
                    "safety. The library features multi-key management, thread-safe operations for reliable requests "
                    "in multi-threaded environments, and automatic fallback to alternate keys when API rate limits "
                    "are reached. Ideal for developers looking to optimize interactions with OpenAI's services in "
                    "robust, concurrent applications.",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        url="https://github.com/CZT0/StableOpenAI.git",
        packages=find_packages(),  # Automatically find all packages
        install_requires=["openai", "backoff"],
        python_requires=">=3.7",
)
