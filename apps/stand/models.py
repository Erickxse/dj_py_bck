from django.db import models
from apps.dashboard.fields import BitBooleanField
# from models import CexCountry 
# Create your models here.

class CexStand(models.Model):
    # Django automáticamente agrega un campo `id` como clave primaria en los modelos,
    # por lo que no es necesario definirlo manualmente.
    id = models.AutoField(primary_key=True)
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
    tour_virtual_active = BitBooleanField(default=False, db_comment='')
    isdeleted = BitBooleanField(default=False, db_comment='')
    isactive = BitBooleanField(default=False, db_comment='')
    credits_total = models.FloatField(db_comment='Valor de crΘditos dados por el plan')
    credits_extra = models.FloatField(db_comment='Valor de crΘditos adquiridos')
    issleep = BitBooleanField(default=False, db_comment='')
    pro_switch = BitBooleanField(default=False, db_comment='')
    pro_slide_image = models.CharField(max_length=255)
    pro_body = models.TextField(blank=True, null=True)
    pro_products = models.TextField()
    pro_services = models.TextField()
    pro_faq = models.TextField()
    pro_products_switch = BitBooleanField(default=False, db_comment='')
    pro_services_switch = BitBooleanField(default=False, db_comment='')
    pro_hv_switch = BitBooleanField(default=False, db_comment='')
    video_code = models.TextField(blank=True, null=True, db_comment='Video del Stand')
    email_manager = models.TextField(blank=True, null=True)
    email_quotes = BitBooleanField(default=False, db_comment='')
    do_related = BitBooleanField(default=False, db_comment='')
    can_sell = BitBooleanField(default=False, db_comment='')
    switch_store = BitBooleanField(default=False, db_comment='')
    store_code = models.TextField(blank=True, null=True)
    professional_type_id = models.IntegerField(blank=True, null=True)
    builder_type_id = models.IntegerField(blank=True, null=True)
    renewal_date = models.DateField(blank=True, null=True)
    state_1 = BitBooleanField(default=False, db_comment='')
    state_2 = BitBooleanField(default=False, db_comment='')
    state_3 = BitBooleanField(default=False, db_comment='')
    state_4 = BitBooleanField(default=False, db_comment='')
    state_5 = BitBooleanField(default=False, db_comment='')
    state_6 = BitBooleanField(default=False, db_comment='')
    state_7 = BitBooleanField(default=False, db_comment='')
    state_8 = BitBooleanField(default=False, db_comment='')
    state_9 = BitBooleanField(default=False, db_comment='')
    state_10 = BitBooleanField(default=False, db_comment='')
    date_activate_shopping = models.DateTimeField(blank=True, null=True)
    delivery_cost = models.FloatField()
    url = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    industry_id = models.IntegerField(blank=True, null=True)
    adsense_code = models.TextField(blank=True, null=True)
    adsense_enabled = BitBooleanField(default=False, db_comment='')
    cex_whatsapp_phone = models.CharField(max_length=30, blank=True, null=True)
    cex_whatsapp_start_date = models.DateField(blank=True, null=True)
    cex_whatsapp_end_date = models.DateField(blank=True, null=True)
    cex_whatsapp_enabled = BitBooleanField(default=False, db_comment='')
    show_map = BitBooleanField(default=False, db_comment='')
    manual_end_date_whatsapp = BitBooleanField(default=False, db_comment='')
    show_product_price = BitBooleanField(default=False, db_comment='')
    percent_price_contruex = models.FloatField()
    percent_price_public_sale = models.FloatField()
    enable_quotes_crm = BitBooleanField(default=False, db_comment='')
    cex_manage_crm_start_date = models.DateField(blank=True, null=True)
    cex_manage_crm_end_date = models.DateField(blank=True, null=True)
    manage_crm = BitBooleanField(default=False, db_comment='')
    manage_client_quotes_crm = BitBooleanField(default=False, db_comment='')
    cex_manage_client_quotes_crm_start_date = models.DateField(blank=True, null=True)
    cex_manage_client_quotes_crm_end_date = models.DateField(blank=True, null=True)
    dealers = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='(DC2Type:json_array)')
    enable_client_quotes_form = BitBooleanField(default=False, db_comment='')
    enable_client_advisory_distributors_form = BitBooleanField(default=False, db_comment='')
    other_trans_emails = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='(DC2Type:json_array)')
    other_users = models.TextField(db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='(DC2Type:json_array)')
    enable_quote_direct = BitBooleanField(default=False, db_comment='')
    enable_super_stand = BitBooleanField(default=False, db_comment='')
    date_activate_super_stand = models.DateTimeField(blank=True, null=True)
    super_stand_id = models.IntegerField(blank=True, null=True)
    country = models.ForeignKey(
        'stand.CexCountry', on_delete=models.DO_NOTHING, related_name='stand_cex')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_stand'
        unique_together = (('slug', 'country_id'),)

class CexPlan(models.Model):
    name = models.CharField(max_length=150, db_comment='Nombre del Plan')
    description = models.CharField(max_length=250, db_comment='Descripci≤n del Plan')
    description_pro = models.CharField(max_length=250, blank=True, null=True, db_comment='Descripci≤n del Plan profecional')
    payment_description = models.CharField(max_length=255, blank=True, null=True)
    payment_description_pro = models.CharField(max_length=255, blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    features_pro = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=45, blank=True, null=True, db_comment='Slug del Plan')
    active = models.TextField(db_comment='Activo/Inactivo')  # This field type is a guess.
    plan_type = models.CharField(max_length=45, db_comment='Tipo del Plan')
    valid_for_days = models.IntegerField(db_comment='Validez del plan en dφas')
    monthly_cost = models.FloatField(db_comment='Costo del plan en valor mensual')
    monthly_cost_pro = models.FloatField(blank=True, null=True, db_comment='Costo del plan en valor mensual - profesional')
    annual_discount = models.FloatField(blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado')
    annual_discount_pro = models.FloatField(blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado - profesional')
    catalogs = models.IntegerField(db_comment='N·mero de catßlogos para el plan')
    catalogs_pro = models.IntegerField(blank=True, null=True, db_comment='N·mero de catßlogos para el plan profesional')
    branding_index = models.TextField(db_comment='Permite modificar landing page exhibidor')  # This field type is a guess.
    branding_index_pro = models.TextField(blank=True, null=True, db_comment='Permite modificar landing page exhibidor - profesional')  # This field type is a guess.
    video_stand = models.TextField(db_comment='Se permite colocar videos en el exhibidor')  # This field type is a guess.
    video_stand_pro = models.TextField(blank=True, null=True, db_comment='Se permite colocar videos en el exhibidor - profesional')  # This field type is a guess.
    slider_pro_stand = models.TextField(db_comment='Permite la incluir de sliders pro')  # This field type is a guess.
    slider_pro_stand_pro = models.TextField(blank=True, null=True, db_comment='Permite la incluir de sliders pro - profesional')  # This field type is a guess.
    tour_virtual_stand = models.TextField(db_comment='Permite incluir Tour virtual')  # This field type is a guess.
    tour_virtual_stand_pro = models.TextField(blank=True, null=True, db_comment='Permite incluir Tour virtual - profesional')  # This field type is a guess.
    featured_product_index = models.IntegerField(db_comment='N·mero de productos destacados en pagina principal')
    featured_product_index_pro = models.IntegerField(blank=True, null=True, db_comment='N·mero de productos destacados en pagina principal - profesional')
    featured_product_category = models.IntegerField(db_comment='N·mero de productos destacados en categorφas')
    featured_product_category_pro = models.IntegerField(blank=True, null=True, db_comment='N·mero de productos destacados en categorφas - profesional')
    featured_catalog_index = models.IntegerField(db_comment='N·mero de catßlogos')
    featured_catalog_index_pro = models.IntegerField(blank=True, null=True, db_comment='N·mero de catßlogos - profesional')
    featured_catalog_category = models.IntegerField(db_comment='Numero de catßlogos promocionados en categorφa')
    featured_catalog_category_pro = models.IntegerField(blank=True, null=True, db_comment='Numero de catßlogos promocionados en categorφa - profesional')
    banner_index = models.IntegerField(db_comment='N·mero de imßgenes por banner')
    banner_index_pro = models.IntegerField(blank=True, null=True, db_comment='N·mero de imßgenes por banner - profesional')
    credits = models.IntegerField(db_comment='CrΘditos para el plan')
    credits_pro = models.IntegerField(blank=True, null=True, db_comment='CrΘditos para el plan profesional')
    tour_virtual_stand_arq = models.TextField(db_comment='Permite incluir Tour virtual Arquitectura')  # This field type is a guess.
    tour_virtual_stand_fer = models.TextField(db_comment='Permite incluir Tour virtual Ferreteria')  # This field type is a guess.
    slider_pro_stand_arq = models.IntegerField(blank=True, null=True, db_comment='Permite la incluir de sliders pro arquitectura')
    slider_pro_stand_fer = models.IntegerField(blank=True, null=True, db_comment='Permite la incluir de sliders pro ferreteria')
    description_arq = models.CharField(max_length=250, blank=True, null=True, db_comment='Descripci≤n del Plan Arquitectura')
    description_fer = models.CharField(max_length=250, blank=True, null=True, db_comment='Descripci≤n del Plan Ferreteria')
    monthly_cost_arq = models.FloatField(blank=True, null=True, db_comment='Costo del plan en valor mensual - Arquitectura')
    monthly_cost_fer = models.FloatField(blank=True, null=True, db_comment='Costo del plan en valor mensual - Ferreteria')
    payment_description_arq = models.CharField(max_length=255, blank=True, null=True)
    payment_description_fer = models.CharField(max_length=255, blank=True, null=True)
    features_arq = models.TextField(blank=True, null=True)
    features_fer = models.TextField(blank=True, null=True)
    annual_discount_arq = models.FloatField(blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado - Arquitectura')
    annual_discount_fer = models.FloatField(blank=True, null=True, db_comment='Descuento en el plan, en caso de pago anualizado - Ferreteria')
    catalogs_arq = models.IntegerField(blank=True, null=True, db_comment='N·mero de catßlogos para el plan Arquitectura')
    catalogs_fer = models.IntegerField(blank=True, null=True, db_comment='N·mero de catßlogos para el plan Ferreteria')
    branding_index_arq = models.TextField(blank=True, null=True, db_comment='Permite modificar landing page exhibidor - Arquitectura')  # This field type is a guess.
    branding_index_fer = models.TextField(blank=True, null=True, db_comment='Permite modificar landing page exhibidor - Ferreteria')  # This field type is a guess.
    video_stand_arq = models.TextField(blank=True, null=True, db_comment='Se permite colocar videos en el exhibidor - Arquitectura')  # This field type is a guess.
    video_stand_fer = models.TextField(blank=True, null=True, db_comment='Se permite colocar videos en el exhibidor - Ferreteria')  # This field type is a guess.
    featured_product_index_arq = models.IntegerField(blank=True, null=True, db_comment='N·mero de productos destacados en pagina principal - Arquitectura')
    featured_product_index_fer = models.IntegerField(blank=True, null=True, db_comment='N·mero de productos destacados en pagina principal - Ferreteria')
    featured_product_category_arq = models.IntegerField(blank=True, null=True, db_comment='N·mero de productos destacados en categorφas - Arquitectura')
    featured_product_category_fer = models.IntegerField(blank=True, null=True, db_comment='N·mero de productos destacados en categorφas - Ferreteria')
    featured_catalog_index_arq = models.IntegerField(blank=True, null=True, db_comment='N·mero de catßlogos - Arquitectura')
    featured_catalog_index_fer = models.IntegerField(blank=True, null=True, db_comment='N·mero de catßlogos - Ferreteria')
    featured_catalog_category_arq = models.IntegerField(blank=True, null=True, db_comment='Numero de catßlogos promocionados en categorφa - Arquitectura')
    featured_catalog_category_fer = models.IntegerField(blank=True, null=True, db_comment='Numero de catßlogos promocionados en categorφa - Ferreteria')
    banner_index_arq = models.IntegerField(blank=True, null=True, db_comment='N·mero de imßgenes por banner - Arquitectura')
    banner_index_fer = models.IntegerField(blank=True, null=True, db_comment='N·mero de imßgenes por banner - Ferreteria')
    credits_arq = models.IntegerField(blank=True, null=True, db_comment='CrΘditos para el plan Arquitectura')
    credits_fer = models.IntegerField(blank=True, null=True, db_comment='CrΘditos para el plan Ferreteria')
    promotion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_plan'


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
        
class CexCountry(models.Model):
    
    iso = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_country'
        

class CexExhibition(models.Model):
    stand_id = models.IntegerField()
    url_image = models.CharField(max_length=250)
    title = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    code = models.TextField(blank=True, null=True)
    date_final = models.DateField(blank=True, null=True)
    slug = models.CharField(max_length=255)
    country = models.ForeignKey(
        CexCountry,  models.DO_NOTHING, related_name='exhibition_cex')

    class Meta:
        managed = False
        db_table = 'cex_exhibition'
        unique_together = (('slug', 'stand_id', 'country_id'),)


class Profile(models.Model):
    user_id = models.IntegerField(primary_key=True, db_comment='dektrium')
    name = models.CharField(max_length=255, db_collation='utf8mb3_general_ci',
                            blank=True, null=True, db_comment='dektrium')
    public_email = models.CharField(
        max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='dektrium')
    gravatar_email = models.CharField(
        max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='dektrium')
    gravatar_id = models.CharField(
        max_length=32, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='dektrium')
    location = models.CharField(max_length=255, db_collation='utf8mb3_general_ci',
                                blank=True, null=True, db_comment='localidad lat,lng')
    website = models.CharField(max_length=255, db_collation='utf8mb3_general_ci',
                               blank=True, null=True, db_comment='Sitio web')
    bio = models.TextField(db_collation='utf8mb3_general_ci',
                           blank=True, null=True, db_comment='Biograf├¡a')
    timezone = models.CharField(max_length=40, db_collation='utf8mb3_general_ci',
                                blank=True, null=True, db_comment='Zona horaria')
    cex_first_name = models.CharField(
        max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True)
    cex_last_name = models.CharField(
        max_length=100, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='Apellido')
    cex_contact_phone = models.CharField(
        max_length=45, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='Tel├®fono de contacto')
    # This field type is a guess.
    cex_newsfeed_subscription = models.TextField(
        blank=True, null=True, db_comment='Subscripci├│n a noticias')
    cex_city = models.CharField(
        max_length=45, db_collation='utf8mb3_general_ci', blank=True, null=True, db_comment='Ciudad')
    cex_country_id = models.IntegerField(
        blank=True, null=True, db_comment='Pais Id')
    cex_province_id = models.IntegerField(blank=True, null=True)
    cex_status = models.CharField(
        max_length=25, db_comment='Status del usuario')
    cex_comments = models.TextField(blank=True, null=True)
    cex_home_address = models.CharField(max_length=255, blank=True, null=True)
    cex_billing_address = models.CharField(
        max_length=255, blank=True, null=True)
    cex_ruc = models.CharField(max_length=13, blank=True, null=True)
    cex_contact_home_phone = models.CharField(max_length=45)
    email_visitor_sent = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'profile'
