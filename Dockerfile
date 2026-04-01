FROM odoo:19.0

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /mnt/extra-addons
COPY ./custom_addons /mnt/extra-addons
COPY ./config/odoo.conf /etc/odoo/odoo.conf

USER odoo
EXPOSE 8069

CMD ["odoo", "-c", "/etc/odoo/odoo.conf"]
