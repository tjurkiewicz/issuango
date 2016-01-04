# Some of the models based on django-oscar

import datetime
import six

import django.conf
import django.contrib.contenttypes.fields as ctfields
import django.contrib.contenttypes.models as ctmodels
import django.core.validators
import django.db.models as models
import django.utils.translation

import treebeard.mp_tree as tree

import issuango.core.validators

import utils

User = django.conf.settings.AUTH_USER_MODEL
_ = django.utils.translation.ugettext_lazy


class Project(models.Model):
    name        = models.CharField(max_length=128)
    key         = models.SlugField()
    attribute_scheme = models.ForeignKey('AttributeScheme')

    individual_roles = models.ManyToManyField(User, through='ProjectRole', related_name='roles')


    def __str__(self):
        return '<{}>'.format(self.name)

    class Meta:
        app_label = 'issue'


class ProjectRole(models.Model):
    project = models.ForeignKey('Project', verbose_name=_('Project'))
    user = models.ForeignKey(User, verbose_name=_('User'))

    READ_ROLE = 'read'
    WRITE_ROLE = 'write'
    ADMIN_ROLE = 'admin'
    ROLE_CHOICES = [
        (READ_ROLE, _('Read')),
        (WRITE_ROLE, _('Write')),
        (ADMIN_ROLE, _('Admin')),
    ]
    role = models.CharField(choices=ROLE_CHOICES, default=ROLE_CHOICES[0][0], max_length=10, verbose_name=_('Role'))

    def __str__(self):
        return '<{0}@{1}: {2}>'.format(self.user, self.project.name, self.role)

    class Meta:
        app_label = 'issue'


class AttributeScheme(models.Model):
    name        = models.CharField(max_length=128)
    code        = models.SlugField(unique=True)

    def __str__(self):
        return '<{}>'.format(self.name)

    class Meta:
        app_label = 'issue'


class Attribute(models.Model):
    attribute_scheme = models.ManyToManyField(AttributeScheme, related_name='attributes', blank=True,
                                    verbose_name=_('Attribute schemas'))
    name = models.CharField(_('Name'), max_length=128)
    code = models.SlugField(_('Code'), max_length=128,
                            validators=[
                                django.core.validators.RegexValidator(
                                    regex=r'^[a-zA-Z_][0-9a-zA-Z_]*$',
                                    message=_(
                                        "Code can only contain the letters a-z, A-Z, digits, "
                                        "and underscores, and can't start with a digit")),
                                issuango.core.validators.non_python_keyword,
                            ])

    # Attribute types
    TEXT     = 'text'
    INTEGER  = 'integer'
    BOOLEAN  = 'boolean'
    FLOAT    = 'float'
    RICHTEXT = 'richtext'
    DATE     = 'date'
    OPTION   = 'option'
    ENTITY   = 'entity'
    FILE     = 'file'
    IMAGE    = 'image'
    TYPE_CHOICES = (
        (TEXT,     _('Text')),
        (INTEGER,  _('Integer')),
        (BOOLEAN , _('True / False')),
        (FLOAT,    _('Float')),
        (RICHTEXT, _('Rich Text')),
        (DATE,     _('Date')),
        (OPTION,   _('Option')),
        (ENTITY,   _('Entity')),
        (FILE,     _('File')),
        (IMAGE,    _('Image')),
    )
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],  max_length=20, verbose_name=_('Type'))

    option_group = models.ForeignKey('AttributeOptionGroup', blank=True, null=True, verbose_name=_('Option Group'),
        help_text=_('Select an option group if using type "Option"'))
    required = models.BooleanField(_('Required'), default=False)


    @property
    def is_file(self):
        return self.type in [self.FILE, self.IMAGE]

    @property
    def is_option(self):
        return self.type == self.OPTION

    def save_value(self, issue, value):
        no_value = lambda: value is None or value == '' or (self.is_file and value is False)

        try:
            attribute_value = issue.attribute_values.get(attribute=self)
        except AttributeValue.DoesNotExist:
            if no_value():
                return
            attribute_value = AttributeValue.objects.create(issue=issue, attribute=self)

        if no_value():
            attribute_value.delete()
        elif value != attribute_value.value:
            attribute_value.value = value
            attribute_value.save()

    def validate_value(self, value):
        validator = getattr(self, '_validate_%s' % self.type)
        validator(value)

    # Validators

    def _validate_text(self, value):
        if not isinstance(value, six.string_types):
            raise django.core.validators.ValidationError(_('Must be str or unicode'))
    _validate_richtext = _validate_text

    def _validate_float(self, value):
        try:
            float(value)
        except ValueError:
            raise django.core.validators.ValidationError(_('Must be a float'))

    def _validate_integer(self, value):
        try:
            int(value)
        except ValueError:
            raise django.core.validators.ValidationError(_('Must be an integer'))

    def _validate_date(self, value):
        if not isinstance(value, (datetime.datetime, datetime.date)):
            raise django.core.validators.ValidationError(_('Must be a date or datetime'))

    def _validate_boolean(self, value):
        if not type(value) == bool:
            raise django.core.validators.ValidationError(_('Must be a boolean'))

    def _validate_entity(self, value):
        if not isinstance(value, models.Model):
            raise django.core.validators.ValidationError(_('Must be a model instance'))

    def _validate_option(self, value):
        if self.is_option and isinstance(value, six.string_types):
            try:
                value = self.option_group.options.get(option=value)
            except AttributeOption.DoesNotExist:
                raise django.core.validators.ValidationError(
                    _('String can replace option value only if it points to valid AttributeOption instance'))

        if not isinstance(value, AttributeOption):
            raise django.core.validators.ValidationError(
                _('Must be an AttributeOption model object instance'))
        if not value.pk:
            raise django.core.validators.ValidationError(_("AttributeOption has not been saved yet"))
        valid_values = self.option_group.options.values_list(
            'option', flat=True)
        if value.option not in valid_values:
            raise django.core.validators.ValidationError(
                _("%(enum)s is not a valid choice for %(attr)s") %
                {'enum': value, 'attr': self})

    def _validate_file(self, value):
        if value and not isinstance(value, File):
            raise django.core.validators.ValidationError(_("Must be a file field"))
    _validate_image = _validate_file

    class Meta:
        app_label = 'issue'


class AttributeOptionGroup(models.Model):
    name = models.CharField(_('Name'), max_length=128)

    class Meta:
        app_label = 'issue'


class AttributeOption(models.Model):
    group  = models.ForeignKey('AttributeOptionGroup', related_name='options', verbose_name=_("Group"))
    option = models.CharField(_('Option'), max_length=255)
    glyph  = models.CharField(_('Bootstrap 3 glyph'), max_length=255)
    icon   = models.ImageField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = 'issue'
        unique_together = ('group', 'option', )


class AttributeValue(models.Model):
    attribute = models.ForeignKey('Attribute', verbose_name=_("Attribute"))
    issue     = models.ForeignKey('Issue', related_name='attribute_values', verbose_name=_("Product"))

    value_text     = models.TextField(_('Text'),           blank=True, null=True)
    value_integer  = models.IntegerField(_('Integer'),     blank=True, null=True)
    value_boolean  = models.NullBooleanField(_('Boolean'), blank=True)
    value_float    = models.FloatField(_('Float'),         blank=True, null=True)
    value_richtext = models.TextField(_('Richtext'),       blank=True, null=True)
    value_date     = models.DateTimeField(_('Date'),       blank=True, null=True)
    value_option   = models.ForeignKey('AttributeOption',  blank=True, null=True, verbose_name=_("Value option"))
    value_file     = models.FileField(max_length=255,      blank=True, null=True)
    value_image    = models.ImageField(max_length=255,     blank=True, null=True)
    value_entity   = ctfields.GenericForeignKey('entity_content_type', 'entity_object_id')

    entity_content_type = models.ForeignKey(ctmodels.ContentType, null=True, blank=True, editable=False)
    entity_object_id    = models.PositiveIntegerField(null=True, blank=True, editable=False)

    @property
    def value(self):
        return getattr(self, 'value_%s' % self.attribute.type)

    @value.setter
    def value(self, new_value):
        if self.attribute.is_option and isinstance(new_value, six.string_types):
            new_value = self.attribute.option_group.options.get(option=new_value)
        setattr(self, 'value_%s' % self.attribute.type, new_value)

    class Meta:
        app_label = 'issue'


class IssueStatus(models.Model):
    glyph = models.CharField(_('Bootstrap 3 glyph'), max_length=255)
    icon = models.ImageField(max_length=255, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=128)


class Issue(models.Model):
    key = django.db.models.SlugField()
    project = django.db.models.ForeignKey(Project)
    status = django.db.models.ForeignKey(IssueStatus, related_name='issues')

    assignee = django.db.models.ForeignKey(User, null=True, blank=True, related_name='assigned_set')
    reporter = django.db.models.ForeignKey(User, related_name='reported_set')

    description = django.db.models.TextField()

    created = django.db.models.DateTimeField(auto_now_add=True)
    updated = django.db.models.DateTimeField(auto_now=True)

    attributes = django.db.models.ManyToManyField('Attribute', through='AttributeValue')

    @property
    def attribute_scheme(self):
        return self.project.attribute_scheme

    def __init__(self, *args, **kwargs):
        super(Issue, self).__init__(*args, **kwargs)
        self.attr = utils.IssueAttributesContainer(issue=self)

    def save(self, *args, **kwargs):
        super(Issue, self).save(*args, **kwargs)
        self.attr.save()

    def clean(self):
        self.attr.validate_attributes()
        super(Issue, self).clean()

    class Meta:
        app_label = 'issue'


