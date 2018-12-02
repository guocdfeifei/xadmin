from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

SERVER_STATUS = (
    (0, u"Normal"),
    (1, u"Down"),
    (2, u"No Connect"),
    (3, u"Error"),
)
SERVICE_TYPES = (
    ('moniter', u"Moniter"),
    ('lvs', u"LVS"),
    ('db', u"Database"),
    ('analysis', u"Analysis"),
    ('admin', u"Admin"),
    ('storge', u"Storge"),
    ('web', u"WEB"),
    ('email', u"Email"),
    ('mix', u"Mix"),
)


@python_2_unicode_compatible
class IDC(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    contact = models.CharField(max_length=32)
    telphone = models.CharField(max_length=32)
    address = models.CharField(max_length=128)
    customer_id = models.CharField(max_length=128)
    groups = models.ManyToManyField(Group)  # many

    create_time = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"IDC"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class Host(models.Model):
    idc = models.ForeignKey(IDC, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    nagios_name = models.CharField(u"Nagios Host ID", max_length=64, blank=True, null=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    internal_ip = models.GenericIPAddressField(blank=True, null=True)
    user = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    ssh_port = models.IntegerField(blank=True, null=True)
    status = models.SmallIntegerField(choices=SERVER_STATUS)

    brand = models.CharField(max_length=64, choices=[(i, i) for i in (u"DELL", u"HP", u"Other")])
    model = models.CharField(max_length=64)
    cpu = models.CharField(max_length=64)
    core_num = models.SmallIntegerField(choices=[(i * 2, "%s Cores" % (i * 2)) for i in range(1, 15)])
    hard_disk = models.IntegerField()
    memory = models.IntegerField()

    system = models.CharField(u"System OS", max_length=32, choices=[(i, i) for i in (u"CentOS", u"FreeBSD", u"Ubuntu")])
    system_version = models.CharField(max_length=32)
    system_arch = models.CharField(max_length=32, choices=[(i, i) for i in (u"x86_64", u"i386")])

    create_time = models.DateField()
    guarantee_date = models.DateField()
    service_type = models.CharField(max_length=32, choices=SERVICE_TYPES)
    description = models.TextField()

    administrator = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Admin")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"Host"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class MaintainLog(models.Model):
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    maintain_type = models.CharField(max_length=32)
    hard_type = models.CharField(max_length=16)
    time = models.DateTimeField()
    operator = models.CharField(max_length=16)
    note = models.TextField()

    def __str__(self):
        return '%s maintain-log [%s] %s %s' % (self.host.name, self.time.strftime('%Y-%m-%d %H:%M:%S'),
                                               self.maintain_type, self.hard_type)

    class Meta:
        verbose_name = u"Maintain Log"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class HostGroup(models.Model):

    name = models.CharField(max_length=32)
    description = models.TextField()
    hosts = models.ManyToManyField(
        Host, verbose_name=u'Hosts', blank=True, related_name='groups')

    class Meta:
        verbose_name = u"Host Group"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class AccessRecord(models.Model):
    date = models.DateField()
    user_count = models.IntegerField()
    view_count = models.IntegerField()

    class Meta:
        verbose_name = u"Access Record"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s Access Record" % self.date.strftime('%Y-%m-%d')

@python_2_unicode_compatible
class kmChoices(models.Model):
  description = models.CharField(max_length=64)

  def __str__(self):
      return self.description

  class Meta:
      verbose_name = u"考试科目"
      verbose_name_plural = verbose_name


@python_2_unicode_compatible
class ccpa(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'

    area = models.CharField(max_length=64, verbose_name=u'报名地区')
    train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    periods = models.CharField(max_length=64, verbose_name=u'期数', choices=[(i, i) for i in (u"一期", u"二期", u"三期")])
    name = models.CharField(max_length=64, verbose_name=u'姓名')
    pinyin = models.CharField(max_length=64, verbose_name=u'姓名拼音')
    sex = models.CharField(max_length=64, verbose_name=u'性别', choices=[(i, i) for i in (u"男", u"女")])
    guarantee_date = models.DateField(verbose_name=u'出生日期')
    nation = models.CharField(max_length=16, verbose_name=u'民族')
    edu = models.CharField(max_length=64, verbose_name=u'学历', choices=[(i, i) for i in (u"本科", u"专科", u"硕士")])
    poilt = models.CharField(max_length=64, verbose_name=u'政治面貌', choices=[(i, i) for i in (u"群众", u"党员")])
    icc = models.CharField(max_length=64, verbose_name=u'身份证号')
    phone = models.CharField(max_length=20, verbose_name=u'手机号')
    email = models.EmailField(error_messages={'invalid': '格式错了.'}, verbose_name=u'联系邮箱')
    school = models.CharField(max_length=64, verbose_name=u'学校')
    specialty = models.CharField(max_length=64, verbose_name=u'专业')
    work = models.CharField(max_length=64, verbose_name=u'工作单位', blank=True, null=True)
    job = models.CharField(max_length=64, verbose_name=u'职务', blank=True, null=True)
    address = models.CharField(max_length=128, verbose_name=u'联系地址')
    enaddress = models.CharField(max_length=128, verbose_name=u'英文地址')
    Postcodes = models.CharField(max_length=16, verbose_name=u'邮编')
    telephone = models.CharField(max_length=16, verbose_name=u'电话')
    type = models.CharField(max_length=64, verbose_name=u'报考类型', choices=[(i, i) for i in (u"CCPA初级", u"CCPA中级", u"CCPA高级")])
    kskm = models.ManyToManyField(kmChoices, verbose_name=u'考试科目')
    exam_date = models.DateField(verbose_name=u'考试时间')
    exam_address = models.CharField(max_length=128, verbose_name=u'考试地点')
    photo = models.ImageField(upload_to='upload/image/%Y/%m', max_length=100, verbose_name=u'上传照片', null=True, blank=True, )
    status = models.CharField(max_length=64,verbose_name=u'报名状态', choices=[(i, i) for i in (u"草稿", u"通过")], default='草稿')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"CCPA报名表"
        verbose_name_plural = verbose_name


@python_2_unicode_compatible
class xss(models.Model):
    # UPLOAD_PATH_IMAGE = 'upload/image/'
    area = models.CharField(max_length=64, verbose_name=u'报名地区')
    train = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="培训机构名称")
    periods = models.CharField(max_length=64, verbose_name=u'期数', choices=[(i, i) for i in (u"一期", u"二期", u"三期")])
    name = models.CharField(max_length=64, verbose_name=u'姓名')
    pinyin = models.CharField(max_length=64, verbose_name=u'姓名拼音')
    sex = models.CharField(max_length=64, verbose_name=u'性别', choices=[(i, i) for i in (u"男", u"女")])
    guarantee_date = models.DateField(verbose_name=u'出生日期')
    nation = models.CharField(max_length=16, verbose_name=u'民族')
    edu = models.CharField(max_length=64, verbose_name=u'学历', choices=[(i, i) for i in (u"本科", u"专科", u"硕士")])
    poilt = models.CharField(max_length=64, verbose_name=u'政治面貌', choices=[(i, i) for i in (u"群众", u"党员")])
    icc = models.CharField(max_length=64, verbose_name=u'身份证号')
    phone = models.CharField(max_length=20, verbose_name=u'手机号')
    email = models.EmailField(error_messages={'invalid': '格式错了.'}, verbose_name=u'联系邮箱')
    # school = models.CharField(max_length=64, verbose_name=u'学校')
    # specialty = models.CharField(max_length=64, verbose_name=u'专业')
    work = models.CharField(max_length=64, verbose_name=u'工作单位', blank=True, null=True)
    job = models.CharField(max_length=64, verbose_name=u'职务', blank=True, null=True)
    address = models.CharField(max_length=128, verbose_name=u'联系地址')
    enaddress = models.CharField(max_length=128, verbose_name=u'英文地址')
    Postcodes = models.CharField(max_length=16, verbose_name=u'邮编')
    telephone = models.CharField(max_length=16, verbose_name=u'电话')
    type = models.CharField(max_length=64, verbose_name=u'报名类型', choices=[(i, i) for i in (u"CCPA《薪税师》一级", u"CCPA《薪税师》二级", u"CCPA《薪税师》三级")])
    # kskm = models.ManyToManyField(kmChoices, verbose_name=u'考试科目')
    below_date = models.DateField(verbose_name=u'线下授课时间')
    exam_date = models.DateField(verbose_name=u'考试时间')
    exam_address = models.CharField(max_length=128, verbose_name=u'考试地点')
    photo = models.ImageField(upload_to='upload/image/%Y/%m', max_length=100, verbose_name=u'上传照片', null=True, blank=True, )
    status = models.CharField(max_length=64,verbose_name=u'报名状态', choices=[(i, i) for i in (u"草稿", u"通过")], default='草稿')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u"薪税师报名表"
        verbose_name_plural = verbose_name
        # permissions = (
        #     ("change_xss_status", "Can change the status of xss"),
        # )
