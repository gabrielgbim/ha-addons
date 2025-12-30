ARG BUILD_FROM
FROM $BUILD_FROM

# Copy root filesystem
COPY rootfs /

# Install Python packages
RUN pip install -r /app/requirements.txt

CMD [ "/run.sh" ]
