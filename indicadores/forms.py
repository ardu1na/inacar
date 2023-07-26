
from django.forms import ModelForm
from indicadores.models import RespuestaObjetivo, RespuestaCompetencia


############### OBJETIVOS
## empleado        
class RespuestaObjetivoEmpleadoForm(ModelForm):
    
    class Meta:
        model = RespuestaObjetivo
        fields = ['resultado_empleado', 'observaciones_empleado']        
## lider
class RespuestaObjetivoLiderForm(ModelForm):
    
    class Meta:
        model = RespuestaObjetivo
        fields = ['resultado_lider', 'observaciones_lider']        
        
############# COMPTENCIAS
## empleado        
class RespuestaCompetenciaEmpleadoForm(ModelForm):
    
    class Meta:
        model = RespuestaCompetencia
        fields = ['descripcion_empleado', 'porcentaje_empleado']        
## lider
class RespuestaCompetenciaLiderForm(ModelForm):
    
    class Meta:
        model = RespuestaCompetencia
        fields = ['descripcion_lider', 'porcentaje_lider']    
        """
        
    
class AdjForm(ModelForm):
    client = CharField(
        widget=TextInput(attrs={
            'class': 'form-control wide mb-3',
            'placeholder': 'type client name...',
            'id': 'client',
            'autocomplete': 'on',
            'list': 'clients',
        })
    )
    service = ModelChoiceField(
        queryset=Service.objects.filter(state=True),
        widget=Select(
            attrs={
                'class': "default-select form-control wide mb-3",
                'id': "service",
                'placeholder': "service",
            }
        ),
        empty_label=' - ',
        required=False  
    )
    
    class Meta:
        model = Adj
        fields = ['notice_date', 'adj_percent',  'type' ]
        
        widgets = {
            
            'notice_date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Notice Date",}),

      
 
            'adj_percent' : TextInput(attrs={'class':"form-control",
            'id':"adj_percent",
            'placeholder':"Adjustment %",}),

            'type' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"type",
                'placeholder' : "type",
                'empty_label': "Account/Service"
                }
            ),
        }

    
class ChangeAdj(ModelForm):
    
    class Meta:
        model = Adj
        fields = ['notice_date', 'adj_percent' ]
        
        widgets = {
            
            'notice_date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Notice Date",}),

      
 
            'adj_percent' : TextInput(attrs={'class':"form-control",
            'id':"adj_percent",
            'placeholder':"Adjustment %",}),

            
        }

class SaleForm(ModelForm):
    
    client = ModelChoiceField(queryset=Client.objects.all(), widget=Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"client",
            'placeholder':"client",}), empty_label = ' - ')

    
    
    sales_rep = ModelChoiceField(queryset=Employee.objects.filter(rol="Sales", active="Yes"), widget=Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"sales_rep",
            'placeholder':"Sales Rep",}), empty_label = ' - ', required=False)

    
    class Meta:
        model = Sale
        
        exclude = ['sale_id', 'revenue', 'change', 'suscription']
        
        
        widgets = {
            
            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),

            'kind' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"service",
                'placeholder' : "Service",
                }
            ),


            'price' : TextInput(attrs={
                'class':"form-control",
                'id':"price",
                'placeholder' : "Price"
                }
            ),
            
            'currency' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"currency",
            'placeholder':"Currency",}),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Notes"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"status",
                'placeholder' : "Status"
                }
            ),

        }


class SaleForm2(ModelForm):
    
    
    
    sales_rep = ModelChoiceField(queryset=Employee.objects.filter(rol="Sales", active="Yes"), widget=Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"sales_rep",
            'placeholder':"Sales Rep",}), empty_label = ' - ',  required=False)
    

    class Meta:
        model = Sale
        
        exclude = ['sale_id', 'revenue', 'change', 'client', 'suscription']
        
        
        widgets = {
            
            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),

            'kind' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"service",
                'placeholder' : "Service",
                }
            ),


            'price' : TextInput(attrs={
                'class':"form-control",
                'id':"price",
                'placeholder' : "Price"
                }
            ),
            
            'currency' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"currency",
            'placeholder':"Currency",}),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Notes"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"status",
                'placeholder' : "Status"
                }
            ),

        }


class ClientSaleForm(ModelForm):
    
    
    
    sales_rep = ModelChoiceField(queryset=Employee.objects.filter(rol="Sales", active="Yes"), widget=Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"sales_rep",
            'placeholder':"Sales Rep",}), empty_label = ' - ',  required=False)
    
    
    
    class Meta:
        model = Sale
        
        exclude = ['id',  'revenue', 'client', 'change']
        
        
        
        widgets = {
            
            
            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),

            'kind' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"service",
                'placeholder' : "Service",
                }
            ),


            'price' : TextInput(attrs={
                'class':"form-control",
                'id':"price",
                'placeholder' : "Price"
                }
            ),
            
            
            'currency' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"currency",
            'placeholder':"Currency",}),
            

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Notes"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"status",
                'placeholder' : "Status",
               
                }
            ),

        }


class CancellService(ModelForm):
    
    id = IntegerField(widget=HiddenInput())
    
    class Meta:
        model = Service
        fields = ['comment_can', 'fail_can', 'date_can']
        
        
        widgets = {
                
            
            'date_can' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Cancellation date",}),
            
            'fail_can' : Select(attrs={
            'class':"default-select form-control wide mb-3",
            'id':"fail_can",
            'placeholder':"Do we fail?",}),
            
            'comment_can' : Textarea(attrs={
                'class':"form-control",
                'id':"comment_can",
                'placeholder' : "Comment"
                }
            ),
        }


class EditSaleForm(ModelForm):
    
    
    
    sales_rep = ModelChoiceField(queryset=Employee.objects.filter(rol="Sales", active="Yes"), widget=Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"sales_rep",
            'placeholder':"Sales Rep",}), empty_label = ' - ',  required=False)

        
    class Meta:
        model = Sale
        
        exclude = ['id', 'revenue', 'client', 'change']
        
        
        
        widgets = {

            'date' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),
            
            'kind' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"kind",
            'placeholder':"Kind",}),

            'comments' : TextInput(attrs={'class':"form-control",
            'id':"comments",
            'placeholder':"Comments",}),

            'service' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"service",
                'placeholder' : "Service",
                }
            ),


            'price' : TextInput(attrs={
                'class':"form-control",
                'id':"price",
                'placeholder' : "Price"
                }
            ),
            
            
            'currency' : Select(attrs={'class':"default-select form-control wide mb-3",
            'id':"currency",
            'placeholder':"Currency",}),

            'note' : TextInput(attrs={
                'class':"form-control",
                'id':"note",
                'placeholder' : "Notes"
                }
            ),

            'cost' : TextInput(attrs={
                'class':"form-control",
                'id':"cost",
                'placeholder' : "Cost"
                }
            ),

            'status' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"status",
                'placeholder' : "Status"
                }
            ),
            

        }
"""