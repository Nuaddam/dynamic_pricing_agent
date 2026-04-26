FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ENV APP_HOME=/app
ENV TZ='Asia/Bangkok'

WORKDIR $APP_HOME

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python -m compileall

# Compile site-packages to improve startup time
RUN python -m compileall $(python -c "import site; print(site.getsitepackages()[0])")

RUN python -m compileall .

ENV OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

CMD exec gunicorn
