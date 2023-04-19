# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    adminid = models.ForeignKey('Instructor', models.DO_NOTHING, db_column='adminID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'admin'


class Course(models.Model):
    course_id = models.CharField(primary_key=True, max_length=8)
    title = models.CharField(max_length=50, blank=True, null=True)
    dept_name = models.ForeignKey('Department', models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'course'


class Department(models.Model):
    dept_name = models.CharField(primary_key=True, max_length=32)
    building = models.CharField(max_length=32, blank=True, null=True)
    budget = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'

        
class Funding(models.Model):
    funding_id = models.CharField(primary_key=True, max_length=8)
    agency = models.CharField(max_length=16, blank=True, null=True)
    amount = models.IntegerField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'funding'


class FundingAwardee(models.Model):
    funding = models.ForeignKey(Funding, models.DO_NOTHING, primary_key=True)
    instructor = models.ForeignKey('Instructor', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'funding_awardee'
        unique_together = (('funding', 'instructor'),)


class Instructor(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=8)  # Field name made lowercase.
    name = models.CharField(max_length=20, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'instructor'
        

class Paper(models.Model):
    paper_id = models.CharField(primary_key=True, max_length=8)
    title = models.CharField(max_length=64, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    publication_venue = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'paper'


class PaperAuthor(models.Model):
    paper = models.ForeignKey(Paper, models.DO_NOTHING, primary_key=True)
    instructor = models.ForeignKey(Instructor, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'paper_author'
        unique_together = (('paper', 'instructor'),)


class Prereq(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, primary_key=True, related_name='prereq_base_course')
    prereq = models.ForeignKey(Course, models.DO_NOTHING, related_name='prereq_required_course')

    class Meta:
        managed = False
        db_table = 'prereq'
        unique_together = (('course', 'prereq'),)


class Section(models.Model):
    course = models.ForeignKey(Course, models.DO_NOTHING, primary_key=True)
    sec_id = models.CharField(max_length=3)
    semester = models.IntegerField()
    year = models.IntegerField()
    building = models.CharField(max_length=32, blank=True, null=True)
    room = models.CharField(max_length=4, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'section'
        unique_together = (('course', 'sec_id', 'semester', 'year'),)


class Student(models.Model):
    student_id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=32, blank=True, null=True)
    dept_name = models.ForeignKey(Department, models.DO_NOTHING, db_column='dept_name', blank=True, null=True)
    total_credits = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'student'


class Takes(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING, primary_key=True, related_name='takes_student')
    course = models.ForeignKey(Section, models.DO_NOTHING, related_name='takes_courseID')
    sec = models.ForeignKey(Section, models.DO_NOTHING, related_name='takes_section')
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name='takes_semester')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', related_name='takes_year')
    grade = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'takes'
        unique_together = (('student', 'course', 'sec', 'semester', 'year'),)


class Teaches(models.Model):
    course = models.ForeignKey(Section, models.DO_NOTHING, primary_key=True, related_name='teaches_courseID')
    sec = models.ForeignKey(Section, models.DO_NOTHING, related_name='teached_section')
    semester = models.ForeignKey(Section, models.DO_NOTHING, db_column='semester', related_name='teaches_semester')
    year = models.ForeignKey(Section, models.DO_NOTHING, db_column='year', related_name='teaches_year')
    teacher = models.ForeignKey(Instructor, models.DO_NOTHING, related_name='teaches_instructor')

    class Meta:
        managed = False
        db_table = 'teaches'
        unique_together = (('course', 'sec', 'semester', 'year', 'teacher'),)


########################################
# Unused Classes
########################################


'''
class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)
        

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
'''