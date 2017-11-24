from django.db import models

# Create your models here.

class DevQuestionnairesHelper(models.Model):
    stem_helper = models.CharField(max_length=512, blank=True, primary_key=True)
    type = models.CharField(max_length=16, blank=True, null=True)
    unit = models.CharField(max_length=512, blank=True, null=True)
    questionnaire_id = models.CharField(max_length=100, blank=True, null=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    first_directory = models.CharField(max_length=100, blank=True, null=True)
    second_directory = models.CharField(max_length=100, blank=True, null=True)
    test_questions_type = models.CharField(max_length=100, blank=True, null=True)
    stem = models.CharField(max_length=1000, blank=True, null=True)
    option_1 = models.CharField(max_length=1000, blank=True, null=True)
    option_2 = models.CharField(max_length=200, blank=True, null=True)
    option_3 = models.CharField(max_length=200, blank=True, null=True)
    option_4 = models.CharField(max_length=200, blank=True, null=True)
    option_5 = models.CharField(max_length=200, blank=True, null=True)
    option_6 = models.CharField(max_length=200, blank=True, null=True)
    option_7 = models.CharField(max_length=200, blank=True, null=True)
    option_8 = models.CharField(max_length=200, blank=True, null=True)
    option_9 = models.CharField(max_length=200, blank=True, null=True)
    option_10 = models.CharField(max_length=200, blank=True, null=True)
    option_11 = models.CharField(max_length=200, blank=True, null=True)
    option_12 = models.CharField(max_length=200, blank=True, null=True)
    option_13 = models.CharField(max_length=200, blank=True, null=True)
    option_14 = models.CharField(max_length=200, blank=True, null=True)
    option_15 = models.CharField(max_length=200, blank=True, null=True)
    option_16 = models.CharField(max_length=200, blank=True, null=True)
    option_17 = models.CharField(max_length=200, blank=True, null=True)
    option_18 = models.CharField(max_length=200, blank=True, null=True)
    option_19 = models.CharField(max_length=200, blank=True, null=True)
    option_20 = models.CharField(max_length=200, blank=True, null=True)
    option_21 = models.CharField(max_length=200, blank=True, null=True)
    option_22 = models.CharField(max_length=200, blank=True, null=True)
    option_23 = models.CharField(max_length=200, blank=True, null=True)
    option_24 = models.CharField(max_length=200, blank=True, null=True)
    option_25 = models.CharField(max_length=200, blank=True, null=True)
    option_26 = models.CharField(max_length=200, blank=True, null=True)
    questionnaire_name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DEV_QUESTIONNAIRES_HELPER'
        unique_together = (('questionnaire_id', 'test_questions_id'),)

class HealthAllChoiceProvStat(models.Model):
    questionnaire_id = models.CharField(max_length=100, blank=True, primary_key=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    organ_level = models.CharField(max_length=20, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    area = models.CharField(max_length=16, blank=True, null=True)
    province_name = models.CharField(max_length=16, blank=True, null=True)
    num = models.FloatField(blank=True, null=True)
    sum_num = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HEALTH_ALL_CHOICE_PROV_STAT'
        unique_together = (('questionnaire_id','test_questions_id','organ_level','options','province_name'),)




class HealthAllMultiStat(models.Model):
    questionnaire_id = models.CharField(max_length=100, blank=True, primary_key=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    organ_level = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=16, blank=True, null=True)
    num = models.FloatField(blank=True, null=True)
    sum_num = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HEALTH_ALL_MULTI_STAT'
        unique_together = (('questionnaire_id', 'test_questions_id', 'organ_level', 'options', 'area'),)

class HealthAllChoiceStat(models.Model):
    questionnaire_id = models.CharField(max_length=100, blank=True, primary_key=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    organ_level = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=16, blank=True, null=True)
    num = models.FloatField(blank=True, null=True)
    sum_num = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HEALTH_ALL_CHOICE_STAT'
        unique_together = (('questionnaire_id', 'test_questions_id', 'organ_level', 'options', 'area'),)



class HospAllChoiceProvStat(models.Model):
    questionnaire_id = models.CharField(max_length=100, blank=True, primary_key=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    gather_level = models.CharField(max_length=100, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    area = models.CharField(max_length=16, blank=True, null=True)
    province_name = models.CharField(max_length=16, blank=True, null=True)
    num = models.FloatField(blank=True, null=True)
    sum_num = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HOSP_ALL_CHOICE_PROV_STAT'
        unique_together = (('questionnaire_id', 'test_questions_id', 'gather_level', 'options', 'area','province_name'),)


class HospAllChoiceStat(models.Model):
    questionnaire_id = models.CharField(max_length=100, blank=True, primary_key=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    gather_level = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=16, blank=True, null=True)
    num = models.FloatField(blank=True, null=True)
    sum_num = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HOSP_ALL_CHOICE_STAT'
        unique_together = (('questionnaire_id', 'test_questions_id', 'gather_level', 'options', 'area'),)

class HospAllMultiProvStat(models.Model):
    questionnaire_id = models.CharField(max_length=100, blank=True, primary_key=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    gather_level = models.CharField(max_length=100, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    area = models.CharField(max_length=16, blank=True, null=True)
    province_name = models.CharField(max_length=16, blank=True, null=True)
    num = models.FloatField(blank=True, null=True)
    sum_num = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HOSP_ALL_MULTI_PROV_STAT'
        unique_together = (('questionnaire_id', 'test_questions_id', 'gather_level', 'options', 'province_name','area'),)

class HospAllMultiStat(models.Model):

    questionnaire_id = models.CharField(max_length=100, blank=True, primary_key=True)
    test_questions_id = models.CharField(max_length=100, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    gather_level = models.CharField(max_length=100, blank=True, null=True)
    area = models.CharField(max_length=16, blank=True, null=True)
    num = models.FloatField(blank=True, null=True)
    sum_num = models.FloatField(blank=True, null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HOSP_ALL_MULTI_STAT'
        unique_together = (('questionnaire_id', 'test_questions_id', 'gather_level', 'options',  'area'),)

class DevQuestions(models.Model):
    qid = models.CharField(max_length=32,primary_key=True)
    tid = models.FloatField(primary_key=True)
    d_type = models.CharField(max_length=16)
    p_type = models.FloatField()
    origin = models.CharField(max_length=2048)
    helper = models.CharField(max_length=2048)
    unit = models.CharField(max_length=8, blank=True, null=True)
    options = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DEV_HELPER'
        unique_together = (('qid', 'tid'),)


class DevOptions(models.Model):
    id = models.BigIntegerField(blank=True, null=True,primary_key=True)
    qid = models.TextField(blank=True, null=True)
    tid = models.BigIntegerField(blank=True, null=True)
    p_type = models.BigIntegerField(blank=True, null=True)
    origin_options = models.TextField(blank=True, null=True)
    options = models.TextField(blank=True, null=True)
    organ_name = models.TextField(blank=True, null=True)
    organ_level = models.TextField(blank=True, null=True)
    gather_level = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    area = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DEV_OPTION'


class DevOptionsDescription(models.Model):
    id = models.FloatField(primary_key=True)
    qid = models.CharField(max_length=16, blank=True, null=True)
    tid = models.FloatField(blank=True, null=True)
    description = models.CharField(max_length=256, blank=True, null=True)
    options = models.CharField(max_length=2048, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DEV_OPTIONS_DESCRIPTION'

class DevOrgan(models.Model):
    questionnaire_id = models.CharField(max_length=100)
    user_id = models.CharField(max_length=100)
    role_id = models.CharField(max_length=100, blank=True, null=True)
    organ_id = models.CharField(max_length=100, blank=True, null=True)
    organ_level = models.CharField(max_length=20, blank=True, null=True)
    city_id = models.CharField(max_length=30, blank=True, null=True)
    province_id = models.CharField(max_length=30, blank=True, null=True)
    class_field = models.CharField(db_column='class', max_length=512, blank=True,
                                   null=True)  # Field renamed because it was a Python reserved word.
    subject = models.CharField(max_length=512, blank=True, null=True)
    organ_name = models.CharField(max_length=120, blank=True, null=True)
    role_name = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    province = models.CharField(max_length=40, blank=True, null=True)
    questionnaire_name = models.CharField(max_length=100, blank=True, null=True)
    questionnaire_status = models.CharField(max_length=100, blank=True, null=True)
    gather_level = models.CharField(max_length=100, blank=True, null=True)
    gather_natural = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DEV_ORGAN'
        unique_together = (('questionnaire_id', 'user_id'),)

class DevPaper(models.Model):
    qid = models.CharField(max_length=100, blank=True, primary_key=True)
    tid = models.CharField(max_length=100, blank=True, null=True)
    organ_level = models.CharField(max_length=20, blank=True, null=True)
    options = models.CharField(max_length=512, blank=True, null=True)
    point = models.CharField(max_length=512, blank=True, null=True)
    area = models.CharField(max_length=20, blank=True, null=True)
    rate = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DEV_PAPER'
        unique_together = (('qid', 'tid'),)

class RateTable(models.Model):
    theme = models.CharField(max_length=14, blank=True, primary_key=True)
    organ_name = models.CharField(max_length=64, blank=True, null=True)
    organ_level = models.CharField(max_length=24, blank=True, null=True)
    gather_level = models.CharField(max_length=24, blank=True, null=True)
    province = models.CharField(max_length=24, blank=True, null=True)
    area = models.CharField(max_length=24, blank=True, null=True)
    o1 = models.CharField(max_length=1024, blank=True, null=True)
    o2 = models.CharField(max_length=1024, blank=True, null=True)
    op1 = models.CharField(max_length=1024, blank=True, null=True)
    op2 = models.CharField(max_length=1024, blank=True, null=True)
    rate = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'RATE_TABLE'
        unique_together = (('theme', 'organ_name','province','area',),)
