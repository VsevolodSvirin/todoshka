FROM swaggerapi/swagger-ui

ADD swagger.yaml /app/

ENV SWAGGER_JSON="/app/swagger.yaml"
