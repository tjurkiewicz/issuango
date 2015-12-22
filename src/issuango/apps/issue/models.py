# Some of the models based on django-oscar

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


class IssueClass(models.Model):
    pass


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
    TEXT     = "text"
    INTEGER  = "integer"
    BOOLEAN  = "boolean"
    FLOAT    = "float"
    RICHTEXT = "richtext"
    DATE     = "date"
    OPTION   = "option"
    ENTITY   = "entity"
    FILE     = "file"
    IMAGE    = "image"
    TYPE_CHOICES = (
        (TEXT,     _("Text")),
        (INTEGER,  _("Integer")),
        (BOOLEAN , _("True / False")),
        (FLOAT,    _("Float")),
        (RICHTEXT, _("Rich Text")),
        (DATE,     _("Date")),
        (OPTION,   _("Option")),
        (ENTITY,   _("Entity")),
        (FILE,     _("File")),
        (IMAGE,    _("Image")),
    )
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0],  max_length=20, verbose_name=_("Type"))

    option_group = models.ForeignKey('AttributeOptionGroup', blank=True, null=True, verbose_name=_("Option Group"),
        help_text=_('Select an option group if using type "Option"'))
    required = models.BooleanField(_('Required'), default=False)


class AttributeOptionGroup(models.Model):
    name = models.CharField(_('Name'), max_length=128)


class AttributeOption(models.Model):
    group  = models.ForeignKey('AttributeOptionGroup', related_name='options', verbose_name=_("Group"))
    option = models.CharField(_('Option'), max_length=255)
    glyph  = models.CharField(_('Bootstrap 3 glyph'), max_length=255)
    icon   = models.ImageField(max_length=255, blank=True, null=True)


class AttributeValue(models.Model):
    attribute = models.ForeignKey('Attribute', verbose_name=_("Attribute"))
    issue = models.ForeignKey('Issue', related_name='attribute_values', verbose_name=_("Product"))

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

    def _get_value(self):
        return getattr(self, 'value_%s' % self.attribute.type)


class Issue(django.db.models.Model):
    key = django.db.models.SlugField()
    project = django.db.models.ForeignKey(Project)

    assignee = django.db.models.ForeignKey(User, null=True, blank=True, related_name='assigned_set')
    reporter = django.db.models.ForeignKey(User, related_name='reported_set')

    description = django.db.models.TextField()

    created = django.db.models.DateTimeField(auto_now_add=True)
    updated = django.db.models.DateTimeField(auto_now=True)

    attributes = django.db.models.ManyToManyField('Attribute', through='AttributeValue')
