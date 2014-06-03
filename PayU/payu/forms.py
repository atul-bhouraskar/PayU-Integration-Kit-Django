from django import forms
from payu.utils import generate_hash, verify_hash

class PayUForm(forms.Form):
    # payu specific fields
    key = forms.CharField()
    hash = forms.CharField(required=False)

    # cart order related fields
    txnid = forms.CharField()
    productinfo = forms.CharField()
    amount = forms.DecimalField(decimal_places=2)

    # buyer details
    firstname = forms.CharField()
    lastname = forms.CharField(required=False)
    email = forms.EmailField()
    phone = forms.RegexField(regex=r'\d{10}', min_length=10, max_length=10)
    address1 = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    country = forms.CharField(required=False)
    zipcode = forms.RegexField(regex=r'\d{6}', min_length=6, max_length=6, required=False)
    
    # merchant's side related fields
    furl = forms.URLField()
    surl = forms.URLField()
    curl = forms.URLField(required=False)
    codurl = forms.URLField(required=False)
    touturl = forms.URLField(required=False)
    udf1 = forms.CharField(required=False)
    udf2 = forms.CharField(required=False)
    udf3 = forms.CharField(required=False)
    udf4 = forms.CharField(required=False)
    udf5 = forms.CharField(required=False)
    pg = forms.CharField(required=False)
    drop_category = forms.CharField(required=False)
    custom_note = forms.CharField(required=False)
    note_category = forms.CharField(required=False)
    service_provider = forms.CharField(initial="payu_paisa")
    
    def __init__(self, data, *args, **kwargs):        
        self.merchant_salt = kwargs.pop('merchant_salt', None)
        if 'hash' not in data:
            data['hash'] = generate_hash(data, 
                                         merchant_salt=self.merchant_salt)
        hide_fields = kwargs.pop('hide_fields', False)
        
        data['service_provider'] = 'payu_paisa'
        super(PayUForm, self).__init__(data, *args, **kwargs)
        
        if hide_fields:
            for name, field in self.fields.items():
                field.widget = forms.HiddenInput()

    
class PayUReturnForm(forms.Form):
    mihpayid = forms.CharField()
    mode = forms.CharField()
    status = forms.CharField()
    key = forms.CharField()
    txnid = forms.CharField()
    amount = forms.DecimalField(decimal_places=2)
    discount = forms.DecimalField(decimal_places=2, required=False)
    productinfo = forms.CharField()
    firstname = forms.CharField()
    lastname = forms.CharField(required=False)
    address1 = forms.CharField(required=False)
    address2 = forms.CharField(required=False)
    city = forms.CharField(required=False)
    state = forms.CharField(required=False)
    country = forms.CharField(required=False)
    zipcode = forms.CharField(required=False)
    email = forms.EmailField()
    phone = forms.CharField()
    udf1 = forms.CharField(required=False)
    udf2 = forms.CharField(required=False)
    udf3 = forms.CharField(required=False)
    udf4 = forms.CharField(required=False)
    udf5 = forms.CharField(required=False)
    hash =  forms.CharField()
    error = forms.CharField(required=False)
    PG_TYPE = forms.CharField()
    bank_ref_num = forms.CharField()
    shipping_firstname = forms.CharField(required=False)
    shipping_lastname = forms.CharField(required=False)
    shipping_address1 = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_city = forms.CharField(required=False)
    shipping_state = forms.CharField(required=False)
    shipping_country = forms.CharField(required=False)
    shipping_zipcode = forms.CharField(required=False)
    shipping_phone = forms.CharField(required=False)
    shipping_phoneverified = forms.CharField(required=False)
    unmappedstatus = forms.CharField()
    payuMoneyId = forms.CharField()
    
    def __init__(self, data, *args, **kwargs):        
        self.merchant_salt = kwargs.pop('merchant_salt', None)
        super(PayUReturnForm, self).__init__(data, *args, **kwargs)
    
    def clean_hash(self):
        hash = self.cleaned_data['hash']
        if not verify_hash(self.data, merchant_salt=self.merchant_salt):
            raise forms.ValidationError("Hash validation failed")
        return hash