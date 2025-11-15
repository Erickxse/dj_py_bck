from django.db import models
from apps.dashboard.fields import BitBooleanField

class User(models.Model):
    username = models.CharField(
        unique=True, max_length=255, db_collation='utf8mb3_general_ci')
    email = models.CharField(unique=True, max_length=255,
                             db_collation='utf8mb3_general_ci')
    password_hash = models.CharField(
        max_length=60, db_collation='utf8mb3_general_ci')
    auth_key = models.CharField(
        max_length=32, db_collation='utf8mb3_general_ci')
    confirmed_at = models.IntegerField(blank=True, null=True)
    unconfirmed_email = models.CharField(
        max_length=255, db_collation='utf8mb3_general_ci', blank=True, null=True)
    blocked_at = models.IntegerField(blank=True, null=True)
    registration_ip = models.CharField(
        max_length=45, db_collation='utf8mb3_general_ci', blank=True, null=True)
    created_at = models.IntegerField()
    updated_at = models.IntegerField()
    flags = models.IntegerField(blank=True, null=True)
    last_login_at = models.IntegerField(blank=True, null=True)
    stand_id = models.IntegerField(blank=True, null=True)
    terms_and_conditions = BitBooleanField(default=False, db_comment='terminos y condiciones aceptados o no aceptados')
    stand_assign = models.IntegerField(blank=True, null=True)
    new_password = models.CharField(
        max_length=60, db_collation='utf8mb3_general_ci', null=False)
    is_complete = BitBooleanField(default=False)
    country_id = models.IntegerField(blank=True, null=False)
    role = models.IntegerField(blank=True, null=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        managed = False
        db_table = 'user'


class AxUserOtp(models.Model):
    email = models.CharField(max_length=255, unique=True,
                             db_collation='utf8mb3_general_ci')
    otp = models.CharField(max_length=6, db_collation='utf8mb3_general_ci')
    created_at = models.DateTimeField()  # Cambiado a DateTimeField
    expires_at = models.DateTimeField()
    verified = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'ax_user_otp'


class CexCountry(models.Model):
    iso = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_country'


class CexProvince(models.Model):
    id = models.IntegerField(primary_key=True)
    country_id = models.IntegerField()
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cex_province'


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
    cex_newsfeed_subscription =  BitBooleanField(default=False, db_comment='Subscripcion a noticias')
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
    tour_virtual_active = BitBooleanField(default=False, db_comment='')
    isdeleted = BitBooleanField(default=False, db_comment='')
    isactive = BitBooleanField(default=False, db_comment='')
    credits_total = models.FloatField(
        db_comment='Valor de crΘditos dados por el plan')
    credits_extra = models.FloatField(
        db_comment='Valor de crΘditos adquiridos')
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
    video_code = models.TextField(
        blank=True, null=True, db_comment='Video del Stand')
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
    cex_manage_client_quotes_crm_start_date = models.DateField(
        blank=True, null=True)
    cex_manage_client_quotes_crm_end_date = models.DateField(
        blank=True, null=True)
    dealers = models.TextField(db_collation='utf8mb3_unicode_ci',
                               blank=True, null=True, db_comment='(DC2Type:json_array)')
    enable_client_quotes_form = BitBooleanField(default=False, db_comment='')
    enable_client_advisory_distributors_form = BitBooleanField(
        default=False, db_comment='')
    other_trans_emails = models.TextField(
        db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='(DC2Type:json_array)')
    other_users = models.TextField(
        db_collation='utf8mb3_unicode_ci', blank=True, null=True, db_comment='(DC2Type:json_array)')
    enable_quote_direct = BitBooleanField(default=False, db_comment='')
    enable_super_stand = BitBooleanField(default=False, db_comment='')
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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'
