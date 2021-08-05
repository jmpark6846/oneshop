def csrf_middleware(get_response):
    # 일회성 구성 및 초기화.

    def middleware(request):
        # 이전에 각 요청에 대해 실행할 코드
        # 뷰 (및 이후의 미들웨어)가 호출됩니다.

        csrftoken = request.COOKIES.get('csrftoken')
        if csrftoken:
            request.META['HTTP_X_CSRFTOKEN'] = csrftoken

        response = get_response(request)

        # 이후 각 요청 / 응답에 대해 실행할 코드
        # 뷰가 호출됩니다.
        return response

    return middleware
