from rest_framework.serializers import ModelSerializer

from .models import (
    Case_Detiles,
    EmpRegistration,
    Registration,
    Set_folder_detils,
    Set_project_detils,
    TextractJob,
    pdf_table_data,
    summary_details,
    whole_data,
    contact_form,
    pdfcount_details,
    UseCases,
    SearchWords,
    file_details,
    farm_details,
    all_results,
)

class all_results_serializers(ModelSerializer):
    class Meta:
        model = all_results
        fields = "__all__"
        
class farm_details_serializers(ModelSerializer):
    class Meta:
        model = farm_details
        fields = "__all__"

class file_details_serializers(ModelSerializer):
    class Meta:
        model = file_details
        fields = "__all__"

class whole_data_serializers(ModelSerializer):
    class Meta:
        model = whole_data
        fields = "__all__"


class Case_Detiles_serializers(ModelSerializer):
    class Meta:
        model = Case_Detiles
        fields = "__all__"


class Registration_serializers(ModelSerializer):
    class Meta:
        model = Registration
        fields = "__all__"


class EmpRegistration_serializers(ModelSerializer):
    class Meta:
        model = EmpRegistration
        fields = "__all__"


class Set_project_detils_serializers(ModelSerializer):
    class Meta:
        model = Set_project_detils
        fields = "__all__"


class Set_folder_detils_serializers(ModelSerializer):
    class Meta:
        model = Set_folder_detils
        fields = "__all__"


class summary_detils_serializers(ModelSerializer):
    class Meta:
        model = summary_details
        fields = "__all__"


class pdf_table_data_serializers(ModelSerializer):
    class Meta:
        model = pdf_table_data
        fields = "__all__"


class contact_form_serializers(ModelSerializer):
    class Meta:
        model = contact_form
        fields = "__all__"


class TextractJob_serializers(ModelSerializer):
    class Meta:
        model = TextractJob
        fields = "__all__"


class Pdfinfo_details_serializers(ModelSerializer):
    class Meta:
        model = pdfcount_details
        fields = "__all__"


class UseCases_serializers(ModelSerializer):
    class Meta:
        model = UseCases
        fields = "__all__"

class SearchWords_serializers(ModelSerializer):
    class Meta:
        model = SearchWords
        fields = "__all__"
