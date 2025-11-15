from django.db import models
from apps.dashboard.fields import BitBooleanField


class CexStand(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    stand_type_id = models.IntegerField()
    seo_id = models.IntegerField()
    stand_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    ruc = models.CharField(max_length=13, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    hits = models.IntegerField(blank=True, null=True)
    slug = models.CharField(max_length=255)
    tour_virtual_code = models.TextField(blank=True, null=True)
    tour_virtual_active = models.TextField()  # This field type is a guess.
    # Field name made lowercase. This field type is a guess.
    isdeleted = models.TextField(
        db_column='isDeleted', db_comment='├Ütil para borrado l├│gico')
    # Field name made lowercase. This field type is a guess.
    isactive = models.TextField(
        db_column='isActive', db_comment='├Ütil para uso de activo/inactivo\n')
    credits_total = models.FloatField(
        db_comment='Valor de cr├®ditos dados por el plan')
    credits_extra = models.FloatField(
        db_comment='Valor de cr├®ditos adquiridos')
    # Field name made lowercase. This field type is a guess.
    issleep = models.TextField(
        db_column='isSleep', db_comment='Verificador de Estado Dormido')
    pro_switch = models.TextField()  # This field type is a guess.
    pro_slide_image = models.CharField(max_length=255)
    pro_body = models.TextField(blank=True, null=True)
    pro_products = models.TextField()
    pro_services = models.TextField()
    pro_faq = models.TextField()
    pro_products_switch = models.TextField()  # This field type is a guess.
    pro_services_switch = models.TextField()  # This field type is a guess.
    # This field type is a guess.
    pro_hv_switch = models.TextField(db_comment='switch horizontal,vertical')
    video_code = models.TextField(
        blank=True, null=True, db_comment='Video del Stand')
    email_manager = models.TextField(blank=True, null=True)
    email_quotes = models.TextField()  # This field type is a guess.
    do_related = models.TextField()  # This field type is a guess.
    can_sell = models.IntegerField()
    switch_store = models.IntegerField()
    store_code = models.TextField(blank=True, null=True)
    professional_type_id = models.IntegerField(blank=True, null=True)
    builder_type_id = models.IntegerField(blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    state_1 = models.TextField()  # This field type is a guess.
    state_2 = models.TextField()  # This field type is a guess.
    state_3 = models.TextField()  # This field type is a guess.
    state_4 = models.TextField()  # This field type is a guess.
    state_5 = models.TextField()  # This field type is a guess.
    state_6 = models.TextField()  # This field type is a guess.
    state_7 = models.TextField()  # This field type is a guess.
    state_8 = models.TextField()  # This field type is a guess.
    state_9 = models.TextField()  # This field type is a guess.
    state_10 = models.TextField()  # This field type is a guess.
    date_activate_shopping = models.DateTimeField(blank=True, null=True)
    delivery_cost = models.FloatField()
    url = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    industry_id = models.IntegerField(blank=True, null=True)
    adsense_code = models.TextField(blank=True, null=True)
    adsense_enabled = models.IntegerField()
    cex_whatsapp_phone = models.CharField(max_length=30, blank=True, null=True)
    cex_whatsapp_start_date = models.DateField(blank=True, null=True)
    cex_whatsapp_end_date = models.DateField(blank=True, null=True)
    cex_whatsapp_enabled = models.IntegerField()
    show_map = models.IntegerField(blank=True, null=True)
    manual_end_date_whatsapp = models.IntegerField(blank=True, null=True)
    show_product_price = models.IntegerField(blank=True, null=True)
    percent_price_contruex = models.FloatField()
    percent_price_public_sale = models.FloatField()
    enable_quotes_crm = models.IntegerField(blank=True, null=True)
    cex_manage_crm_start_date = models.DateField(blank=True, null=True)
    cex_manage_crm_end_date = models.DateField(blank=True, null=True)
    manage_crm = models.IntegerField(blank=True, null=True)
    manage_client_quotes_crm = models.IntegerField(blank=True, null=True)
    cex_manage_client_quotes_crm_start_date = models.DateField(
        blank=True, null=True)
    cex_manage_client_quotes_crm_end_date = models.DateField(
        blank=True, null=True)
    dealers = models.TextField(db_collation='utf8mb3_unicode_ci',
                               blank=True, null=True, db_comment='(DC2Type:json_array)')
    enable_client_quotes_form = models.IntegerField(blank=True, null=True)
    enable_client_advisory_distributors_form = models.IntegerField(
        blank=True, null=True)
    other_trans_emails = models.TextField(
        db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='(DC2Type:json_array)')
    other_users = models.TextField(
        db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='(DC2Type:json_array)')
    enable_quote_direct = models.IntegerField(blank=True, null=True)
    enable_super_stand = models.IntegerField(blank=True, null=True)
    date_activate_super_stand = models.DateTimeField(blank=True, null=True)
    super_stand_id = models.IntegerField(blank=True, null=True)
    country_id = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_stand'
        unique_together = (('slug', 'country_id'),)


class CexSubscription(models.Model):
    creation_date = models.CharField(max_length=45)
    active = models.IntegerField(blank=True, null=True)
    stand_id = models.IntegerField()
    plan_id = models.IntegerField()
    plan_valid_for = models.IntegerField()
    note = models.CharField(max_length=250, blank=True, null=True)
    edit_user = models.IntegerField(blank=True, null=True)
    months = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cex_subscription'
        db_table_comment = 'Gestion de suscripciones construex'


class CexPlan(models.Model):
    name = models.CharField(max_length=150, db_comment='Nombre del Plan')
    description = models.CharField(
        max_length=250, db_comment='Descripci≤n del Plan')
    description_pro = models.CharField(
        max_length=250, blank=True, null=True, db_comment='Descripci≤n del Plan profecional')
    payment_description = models.CharField(
        max_length=255, blank=True, null=True)
    payment_description_pro = models.CharField(
        max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    features_pro = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=45, blank=True,
                            null=True, db_comment='Slug del Plan')
    # This field type is a guess.
    active = models.TextField(db_comment='Activo/Inactivo')
    plan_type = models.CharField(max_length=45, db_comment='Tipo del Plan')
    valid_for_days = models.IntegerField(db_comment='Validez del plan en dφas')
    monthly_cost = models.FloatField(
        db_comment='Costo del plan en valor mensual')
    monthly_cost_pro = models.FloatField(
        blank=True, null=True, db_comment='Costo del plan en valor mensual - profesional')
    annual_discount = models.FloatField(
        blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado')
    annual_discount_pro = models.FloatField(
        blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado - profesional')
    catalogs = models.IntegerField(
        db_comment='N·mero de catßlogos para el plan')
    catalogs_pro = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de catßlogos para el plan profesional')
    # This field type is a guess.
    branding_index = models.TextField(
        db_comment='Permite modificar landing page exhibidor')
    # This field type is a guess.
    branding_index_pro = models.TextField(
        blank=True, null=True, db_comment='Permite modificar landing page exhibidor - profesional')
    # This field type is a guess.
    video_stand = models.TextField(
        db_comment='Se permite colocar videos en el exhibidor')
    # This field type is a guess.
    video_stand_pro = models.TextField(
        blank=True, null=True, db_comment='Se permite colocar videos en el exhibidor - profesional')
    # This field type is a guess.
    slider_pro_stand = models.TextField(
        db_comment='Permite la incluir de sliders pro')
    # This field type is a guess.
    slider_pro_stand_pro = models.TextField(
        blank=True, null=True, db_comment='Permite la incluir de sliders pro - profesional')
    # This field type is a guess.
    tour_virtual_stand = models.TextField(
        db_comment='Permite incluir Tour virtual')
    # This field type is a guess.
    tour_virtual_stand_pro = models.TextField(
        blank=True, null=True, db_comment='Permite incluir Tour virtual - profesional')
    featured_product_index = models.IntegerField(
        db_comment='N·mero de productos destacados en pagina principal')
    featured_product_index_pro = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de productos destacados en pagina principal - profesional')
    featured_product_category = models.IntegerField(
        db_comment='N·mero de productos destacados en categorφas')
    featured_product_category_pro = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de productos destacados en categorφas - profesional')
    featured_catalog_index = models.IntegerField(
        db_comment='N·mero de catßlogos')
    featured_catalog_index_pro = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de catßlogos - profesional')
    featured_catalog_category = models.IntegerField(
        db_comment='Numero de catßlogos promocionados en categorφa')
    featured_catalog_category_pro = models.IntegerField(
        blank=True, null=True, db_comment='Numero de catßlogos promocionados en categorφa - profesional')
    banner_index = models.IntegerField(
        db_comment='N·mero de imßgenes por banner')
    banner_index_pro = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de imßgenes por banner - profesional')
    credits = models.IntegerField(db_comment='CrΘditos para el plan')
    credits_pro = models.IntegerField(
        blank=True, null=True, db_comment='CrΘditos para el plan profesional')
    # This field type is a guess.
    tour_virtual_stand_arq = models.TextField(
        db_comment='Permite incluir Tour virtual Arquitectura')
    # This field type is a guess.
    tour_virtual_stand_fer = models.TextField(
        db_comment='Permite incluir Tour virtual Ferreteria')
    slider_pro_stand_arq = models.IntegerField(
        blank=True, null=True, db_comment='Permite la incluir de sliders pro arquitectura')
    slider_pro_stand_fer = models.IntegerField(
        blank=True, null=True, db_comment='Permite la incluir de sliders pro ferreteria')
    description_arq = models.CharField(
        max_length=250, blank=True, null=True, db_comment='Descripci≤n del Plan Arquitectura')
    description_fer = models.CharField(
        max_length=250, blank=True, null=True, db_comment='Descripci≤n del Plan Ferreteria')
    monthly_cost_arq = models.FloatField(
        blank=True, null=True, db_comment='Costo del plan en valor mensual - Arquitectura')
    monthly_cost_fer = models.FloatField(
        blank=True, null=True, db_comment='Costo del plan en valor mensual - Ferreteria')
    payment_description_arq = models.CharField(
        max_length=255, blank=True, null=True)
    payment_description_fer = models.CharField(
        max_length=255, blank=True, null=True)
    features_arq = models.TextField(blank=True, null=True)
    features_fer = models.TextField(blank=True, null=True)
    annual_discount_arq = models.FloatField(
        blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado - Arquitectura')
    annual_discount_fer = models.FloatField(
        blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado - Ferreteria')
    catalogs_arq = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de catßlogos para el plan Arquitectura')
    catalogs_fer = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de catßlogos para el plan Ferreteria')
    # This field type is a guess.
    branding_index_arq = models.TextField(
        blank=True, null=True, db_comment='Permite modificar landing page exhibidor - Arquitectura')
    # This field type is a guess.
    branding_index_fer = models.TextField(
        blank=True, null=True, db_comment='Permite modificar landing page exhibidor - Ferreteria')
    # This field type is a guess.
    video_stand_arq = models.TextField(
        blank=True, null=True, db_comment='Se permite colocar videos en el exhibidor - Arquitectura')
    # This field type is a guess.
    video_stand_fer = models.TextField(
        blank=True, null=True, db_comment='Se permite colocar videos en el exhibidor - Ferreteria')
    featured_product_index_arq = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de productos destacados en pagina principal - Arquitectura')
    featured_product_index_fer = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de productos destacados en pagina principal - Ferreteria')
    featured_product_category_arq = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de productos destacados en categorφas - Arquitectura')
    featured_product_category_fer = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de productos destacados en categorφas - Ferreteria')
    featured_catalog_index_arq = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de catßlogos - Arquitectura')
    featured_catalog_index_fer = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de catßlogos - Ferreteria')
    featured_catalog_category_arq = models.IntegerField(
        blank=True, null=True, db_comment='Numero de catßlogos promocionados en categorφa - Arquitectura')
    featured_catalog_category_fer = models.IntegerField(
        blank=True, null=True, db_comment='Numero de catßlogos promocionados en categorφa - Ferreteria')
    banner_index_arq = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de imßgenes por banner - Arquitectura')
    banner_index_fer = models.IntegerField(
        blank=True, null=True, db_comment='N·mero de imßgenes por banner - Ferreteria')
    credits_arq = models.IntegerField(
        blank=True, null=True, db_comment='CrΘditos para el plan Arquitectura')
    credits_fer = models.IntegerField(
        blank=True, null=True, db_comment='CrΘditos para el plan Ferreteria')
    promotion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_plan'
