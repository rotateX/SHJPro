from django.db import models
from django.utils.timezone import now
from mdeditor.fields import MDTextField

# Create your models here.


# 创建分类，Category
class Category(models.Model):
    name = models.CharField(verbose_name='类别名称', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '类别名称'
        verbose_name_plural = '类别列表'
        db_table = 'shj_category'  # 数据库表名


# 创建标签，
class Tag(models.Model):
    name = models.CharField(verbose_name='标签名称', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '类别名称'
        verbose_name_plural = '标签列表'
        db_table = 'shj_tag'  # 数据库表名


# 创建内容详情，Content
class Content(models.Model):
    title = models.CharField(verbose_name='作品名称', max_length=24)
    content = MDTextField(verbose_name='正文', blank=True, null=True)
    created_age = models.CharField(verbose_name='创建年代', max_length=20, blank=True, null=True)
    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    pub_time = models.DateTimeField(verbose_name='发布时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False, verbose_name='类别名称', related_name='category')
    tag = models.ManyToManyField(Tag, verbose_name='标签集合', blank=True)
    comment_num = models.PositiveIntegerField(verbose_name='评论数', default=0)
    img = models.ImageField(verbose_name='封面图', null=True, upload_to='contentimages/', default='/contentimages/default.jpg', max_length=255)

    def __str__(self):
        return self.title

    # 更新浏览量 view
    def up_view(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 更新评论数量
    def up_comment(self):
        self.comment_num += 1
        self.save(update_fields=['comment_num'])

    # 下一篇
    def next_article(self):
        return Content.objects.filter(id__gt=self.id, category_id=self.category_id, pub_time__isnull=False,).order_by('id').first()

    # 上一篇
    def pre_article(self):
        return Content.objects.filter(id__lt=self.id, category_id=self.category_id, pub_time__isnull=False).order_by('-id').first()

    class Meta:
        ordering = ['-pub_time']
        verbose_name = '作品'
        verbose_name_plural = '作品列表'
        get_latest_by = 'put_time'
        db_table = 'shj_content'  # 数据库表名



# 创建评论 comment
class Comment(models.Model):
    name = models.CharField(verbose_name='发布人', max_length=15)
    email = models.EmailField(verbose_name='邮箱')
    created_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='文章评论', verbose_name='评论文章')
    body = MDTextField(max_length=250, verbose_name='评论内容')
    active = models.BooleanField(default=False, verbose_name='显示评论')

    def __str__(self):
        return 'Comments by {} on {}'.format(self.name, self.content)

    class Meta:
        ordering = ['created_time']
        verbose_name = '评论'
        verbose_name_plural = '评论列表'
        db_table = 'shj_comment'

