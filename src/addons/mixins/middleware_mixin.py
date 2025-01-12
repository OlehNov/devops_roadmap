from asgiref.sync import iscoroutinefunction, markcoroutinefunction, sync_to_async


class MiddlewareMixin:
    sync_capable = True  # Indicates compatibility with synchronous requests.
    async_capable = True  # Indicates compatibility with asynchronous requests.

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response (callable): The next middleware or view in the chain.

        Raises:
            ValueError: If `get_response` is not provided.
        """
        if get_response is None:
            raise ValueError("get_response must be provided.")
        self.get_response = get_response
        self._async_check()  # Detects if the response is asynchronous.
        super().__init__()

    def __repr__(self):
        """
        Generate a string representation of the middleware instance.

        Returns:
            str: The string representation, including the class and `get_response`.
        """
        return "<%s get_response=%s>" % (
            self.__class__.__qualname__,
            getattr(
                self.get_response,
                "__qualname__",
                self.get_response.__class__.__name__,
            ),
        )

    def _async_check(self):
        """
        Check if `get_response` is an asynchronous function.

        If it is, the middleware is marked as async-capable and will handle requests
        asynchronously when needed.
        """
        if iscoroutinefunction(self.get_response):
            markcoroutinefunction(self)

    def __call__(self, request):
        """
        Handle incoming requests synchronously.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The processed HTTP response.
        """
        if iscoroutinefunction(self):
            # Delegate to the asynchronous call if applicable.
            return self.__acall__(request)

        response = None
        if hasattr(self, "process_request"):
            # Process the request if the method is defined.
            response = self.process_request(request)

        response = response or self.get_response(request)

        if hasattr(self, "process_response"):
            # Process the response if the method is defined.
            response = self.process_response(request, response)

        return response

    async def __acall__(self, request):
        """
        Handle incoming requests asynchronously.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The processed HTTP response.
        """
        response = None
        if hasattr(self, "process_request"):
            # Process the request asynchronously.
            response = await sync_to_async(
                self.process_request,
                thread_sensitive=True,
            )(request)

        response = response or await self.get_response(request)

        if hasattr(self, "process_response"):
            # Process the response asynchronously.
            response = await sync_to_async(
                self.process_response,
                thread_sensitive=True,
            )(request, response)

        return response
