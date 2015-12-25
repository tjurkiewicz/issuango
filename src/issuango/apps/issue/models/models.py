# Some of the models based on django-oscar

import six

import django.conf
import django.contrib.contenttypes.fields as ctfields
import django.contrib.contenttypes.models as ctmodels
import django.core.validators
import django.db.models as models
import django.utils.translation

import issuango.core.validators


User = django.conf.settings.AUTH_USER_MODEL
_ = django.utils.translation.ugettext_lazy


class Project(models.Model):
    name        = models.CharField(max_length=128)
    key         = models.SlugField()
    issue_class = django.db.models.ForeignKey('IssueClass')

    def __str__(self):
        return self.name


class IssueClass(models.Model):
    name        = models.CharField(max_length=128)
    code        = models.SlugField()

    def __str__(self):
        return '<{}>'.format(self.name)


class Attribute(models.Model):
    issue_class = models.ForeignKey('IssueClass', related_name='attributes', blank=True, null=True,
                                    verbose_name=_("Issue class"))
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

    @property
    def is_boolean(self):
        return self.type == self.BOOLEAN

    def save_value(self, issue, value):
        no_value = lambda: (value is None and not self.is_boolean) or value == '' or (self.is_file and value is False)

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


class AttributeOptionGroup(models.Model):
    name = models.CharField(_('Name'), max_length=128)


class AttributeOption(models.Model):
    group  = models.ForeignKey('AttributeOptionGroup', related_name='options', verbose_name=_("Group"))
    option = models.CharField(_('Option'), max_length=255)
    glyph  = models.CharField(_('Bootstrap 3 glyph'), max_length=255)
    icon   = models.ImageField(max_length=255, blank=True, null=True)


class AttributeValue(models.Model):
    attribute = models.ForeignKey('Attribute', verbose_name=_("Attribute"))
    issue     = models.ForeignKey('Issue', related_name='attribute_values', verbose_name=_("Product"))

    value_text     = models.TextField(_('Text'),           blank=True, null=True)
    value_integer  = models.IntegerField(_('Integer'),     blank=True, null=True)
    value_boolean  = models.NullBooleanField(_('Boolean'), blank=True)
    value_float    = models.FloatField(_('Float'),         blank=True, null=True)
    value_richtext = models.TextField(_('Richtext'),       blank=True, null=True)
    value_date     = models.DateField(_('Date'),           blank=True, null=True)
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


class Issue(django.db.models.Model):
    key     = django.db.models.SlugField()
    project = django.db.models.ForeignKey(Project)

    assignee = django.db.models.ForeignKey(User, null=True, blank=True, related_name='assigned_set')
    reporter = django.db.models.ForeignKey(User, related_name='reported_set')

    description = django.db.models.TextField()

    created = django.db.models.DateTimeField(auto_now_add=True)
    updated = django.db.models.DateTimeField(auto_now=True)

    attributes = django.db.models.ManyToManyField('Attribute', through='AttributeValue')

    @property
    def issue_class(self):
        return self.project.issue_class

    def __init__(self, *args, **kwargs):
        super(Issue, self).__init__(*args, **kwargs)
        self.attr = IssueAttributesContainer(issue=self)

    def save(self, *args, **kwargs):
        super(Issue, self).save(*args, **kwargs)
        self.attr.save()


class IssueAttributesContainer(object):
    """
    Stolen liberally from django-eav, but simplified to be product-specific

    To set attributes on an issue, use the `attr` attribute:

        issue.attr.weight = 125
    """

    def __setstate__(self, state):
        self.__dict__ = state
        self.initialised = False

    def __init__(self, issue):
        self.issue = issue
        self.initialised = False

    def __getattr__(self, name):
        if not name.startswith('_') and not self.initialised:
            values = self.get_values().select_related('attribute')
            for v in values:
                setattr(self, v.attribute.code, v.value)
            self.initialised = True
            return getattr(self, name)
        raise AttributeError(
            _("%(obj)s has no attribute named '%(attr)s'") % {
                'obj': self.issue.issue_class, 'attr': name})

    def validate_attributes(self):
        for attribute in self.get_all_attributes():
            value = getattr(self, attribute.code, None)
            if value is None:
                if attribute.required:
                    raise django.core.validators.ValidationError(
                        _("%(attr)s attribute cannot be blank") %
                        {'attr': attribute.code})
            else:
                try:
                    attribute.validate_value(value)
                except django.core.validators.ValidationError as e:
                    raise django.core.validators.ValidationError(
                        _("%(attr)s attribute %(err)s") %
                        {'attr': attribute.code, 'err': e})

    def get_values(self):
        return self.issue.attribute_values.all()

    def get_value_by_attribute(self, attribute):
        return self.get_values().get(attribute=attribute)

    def get_all_attributes(self):
        return self.issue.issue_class.attributes.all()

    def get_attribute_by_code(self, code):
        return self.get_all_attributes().get(code=code)

    def __iter__(self):
        return iter(self.get_values())

    def save(self):
        for attribute in self.get_all_attributes():
            if hasattr(self, attribute.code):
                value = getattr(self, attribute.code)
                attribute.save_value(self.issue, value)

