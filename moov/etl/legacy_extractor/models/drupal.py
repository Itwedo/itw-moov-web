from peewee import *


database = MySQLDatabase(
    "c1moov",
    charset="utf8",
    sql_mode="PIPES_AS_CONCAT",
    use_unicode=True,
    user="root",
    password="Xperia12#",
)


class BaseModel(Model):
    class Meta:
        database = database

    def get_node(self):
        if hasattr(self, "nid"):
            return Node.get_or_none(Node.nid == self.nid)
        return None

    def get_user(self):
        if hasattr(self, "uid"):
            return Users.get_or_none(Users.uid == self.uid)
        return None

    def get_comment(self):
        if hasattr(self, "cid"):
            return Comment.get_or_none(Comment.cid == self.cid)
        return None

    def get_tag(self):
        if hasattr(self, "tid"):
            return TaxonomyTermData.get_or_none(
                TaxonomyTermData.tid == self.tid
            )
        return None

    def get_category(self):
        if hasattr(self, "vid"):
            return TaxonomyVocabulary.get_or_none(
                TaxonomyVocabulary.vid == self.vid
            )
        return None


class Actions(BaseModel):
    aid = CharField(constraints=[SQL("DEFAULT '0'")], primary_key=True)
    callback = CharField(constraints=[SQL("DEFAULT ''")])
    label = CharField(constraints=[SQL("DEFAULT '0'")])
    parameters = TextField()
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_actions"


class AdvpollElectoralList(BaseModel):
    nid = IntegerField()
    uid = IntegerField()

    class Meta:
        table_name = "moov_advpoll_electoral_list"
        indexes = ((("nid", "uid"), True),)
        primary_key = CompositeKey("nid", "uid")


class AggregatorCategory(BaseModel):
    cid = AutoField()
    block = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField()
    title = CharField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = "moov_aggregator_category"


class AggregatorCategoryFeed(BaseModel):
    cid = IntegerField(constraints=[SQL("DEFAULT 0")])
    fid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_aggregator_category_feed"
        indexes = ((("cid", "fid"), True),)
        primary_key = CompositeKey("cid", "fid")


class AggregatorCategoryItem(BaseModel):
    cid = IntegerField(constraints=[SQL("DEFAULT 0")])
    iid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_aggregator_category_item"
        indexes = ((("cid", "iid"), True),)
        primary_key = CompositeKey("cid", "iid")


class AggregatorFeed(BaseModel):
    fid = AutoField()
    block = IntegerField(constraints=[SQL("DEFAULT 0")])
    checked = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField()
    etag = CharField(constraints=[SQL("DEFAULT ''")])
    hash = CharField(constraints=[SQL("DEFAULT ''")])
    image = TextField()
    link = TextField()
    modified = IntegerField(constraints=[SQL("DEFAULT 0")])
    queued = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    refresh = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    url = TextField(index=True)

    class Meta:
        table_name = "moov_aggregator_feed"


class AggregatorItem(BaseModel):
    iid = AutoField()
    fid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    author = CharField(constraints=[SQL("DEFAULT ''")])
    description = TextField()
    guid = TextField()
    link = TextField()
    timestamp = IntegerField(index=True, null=True)
    title = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_aggregator_item"


class Authmap(BaseModel):
    aid = AutoField()
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])
    authname = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    module = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_authmap"
        indexes = ((("uid", "module"), False),)


class AutoarchDate(BaseModel):
    nid = AutoField()
    date = IntegerField(null=True)

    class Meta:
        table_name = "moov_autoarch_date"


class AutoarchState(BaseModel):
    nid = AutoField()
    mode = CharField(null=True)
    state = CharField(null=True)

    class Meta:
        table_name = "moov_autoarch_state"


class AutoassignrolePage(BaseModel):
    display = IntegerField()
    menu = CharField()
    path = TextField()
    rid_page_id = AutoField()
    rids = CharField()
    title = TextField()

    class Meta:
        table_name = "moov_autoassignrole_page"


class Batch(BaseModel):
    bid = AutoField()
    batch = TextField(null=True)
    timestamp = IntegerField()
    token = CharField(index=True)

    class Meta:
        table_name = "moov_batch"


class Block(BaseModel):
    bid = AutoField()
    cache = IntegerField(constraints=[SQL("DEFAULT 1")])
    css_class = CharField(constraints=[SQL("DEFAULT ''")])
    custom = IntegerField(constraints=[SQL("DEFAULT 0")])
    delta = CharField(constraints=[SQL("DEFAULT '0'")])
    module = CharField(constraints=[SQL("DEFAULT ''")])
    options = TextField(null=True)
    pages = TextField()
    region = CharField(constraints=[SQL("DEFAULT ''")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    theme = CharField(constraints=[SQL("DEFAULT ''")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    visibility = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_block"
        indexes = (
            (("theme", "module", "delta"), True),
            (("theme", "status", "region", "weight", "module"), False),
        )


class BlockCustom(BaseModel):
    bid = AutoField()
    body = TextField(null=True)
    format = CharField(null=True)
    info = CharField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = "moov_block_custom"


class BlockNodeType(BaseModel):
    delta = CharField()
    module = CharField()
    type = CharField(index=True)

    class Meta:
        table_name = "moov_block_node_type"
        indexes = ((("module", "delta", "type"), True),)
        primary_key = CompositeKey("delta", "module", "type")


class BlockRole(BaseModel):
    rid = IntegerField(index=True)
    delta = CharField()
    module = CharField()

    class Meta:
        table_name = "moov_block_role"
        indexes = ((("module", "delta", "rid"), True),)
        primary_key = CompositeKey("delta", "module", "rid")


class BlockedIps(BaseModel):
    iid = AutoField()
    ip = CharField(constraints=[SQL("DEFAULT ''")], index=True)

    class Meta:
        table_name = "moov_blocked_ips"


class Cache(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache"


class CacheAdminMenu(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_admin_menu"


class CacheBlock(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_block"


class CacheBootstrap(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_bootstrap"


class CacheCustomfilter(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_customfilter"


class CacheFeatures(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_features"


class CacheFeedsHttp(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_feeds_http"


class CacheField(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_field"


class CacheFilter(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_filter"


class CacheForm(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_form"


class CacheHttpResponseHeaders(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_http_response_headers"


class CacheImage(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_image"


class CacheL10NUpdate(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_l10n_update"


class CacheLibraries(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_libraries"


class CacheMenu(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_menu"


class CacheMetatag(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_metatag"


class CachePage(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_page"


class CachePath(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_path"


class CachePathBreadcrumbs(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_path_breadcrumbs"


class CacheRules(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_rules"


class CacheSmartIp(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_smart_ip"


class CacheToken(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_token"


class CacheUpdate(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_update"


class CacheVariable(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_variable"


class CacheViews(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_cache_views"


class CacheViewsData(BaseModel):
    cid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    serialized = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = "moov_cache_views_data"


class CaptchaPoints(BaseModel):
    captcha_type = CharField(null=True)
    form_id = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    module = CharField(null=True)

    class Meta:
        table_name = "moov_captcha_points"


class CaptchaSessions(BaseModel):
    attempts = IntegerField(constraints=[SQL("DEFAULT 0")])
    csid = AutoField()
    form_id = CharField()
    ip_address = CharField(null=True)
    sid = CharField(constraints=[SQL("DEFAULT ''")])
    solution = CharField(constraints=[SQL("DEFAULT ''")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    token = CharField(null=True)
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_captcha_sessions"
        indexes = ((("csid", "ip_address"), False),)


class CkeditorInputFormat(BaseModel):
    format = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_ckeditor_input_format"
        indexes = ((("name", "format"), True),)
        primary_key = CompositeKey("format", "name")


class CkeditorSettings(BaseModel):
    name = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    settings = TextField(null=True)

    class Meta:
        table_name = "moov_ckeditor_settings"


class Comment(BaseModel):
    cid = AutoField()
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    pid = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    changed = IntegerField(constraints=[SQL("DEFAULT 0")])
    created = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    homepage = CharField(null=True)
    hostname = CharField(constraints=[SQL("DEFAULT ''")])
    language = CharField(constraints=[SQL("DEFAULT ''")])
    mail = CharField(null=True)
    name = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    subject = CharField(constraints=[SQL("DEFAULT ''")])
    thread = CharField()

    class Meta:
        table_name = "moov_comment"
        indexes = (
            (("nid", "language"), False),
            (("nid", "status", "created", "cid", "thread"), False),
            (("pid", "status"), False),
        )

    def get_body(self):
        return FieldDataCommentBody.get_or_none(
            FieldDataCommentBody.entity_id == self.cid
        )


class ConditionalFields(BaseModel):
    dependee = IntegerField()
    dependent = IntegerField()
    options = TextField()

    class Meta:
        table_name = "moov_conditional_fields"


class ContentAccess(BaseModel):
    nid = AutoField()
    settings = TextField(null=True)

    class Meta:
        table_name = "moov_content_access"


class ContentLock(BaseModel):
    ajax_key = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = AutoField()
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_content_lock"


class CtoolsCssCache(BaseModel):
    cid = CharField(primary_key=True)
    css = TextField(null=True)
    filename = CharField(null=True)
    filter = IntegerField(null=True)

    class Meta:
        table_name = "moov_ctools_css_cache"


class CtoolsObjectCache(BaseModel):
    data = TextField(null=True)
    name = CharField()
    obj = CharField()
    sid = CharField()
    updated = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_ctools_object_cache"
        indexes = ((("sid", "obj", "name"), True),)
        primary_key = CompositeKey("name", "obj", "sid")


class CustomfilterFilter(BaseModel):
    cache = IntegerField(constraints=[SQL("DEFAULT 1")])
    description = TextField(null=True)
    fid = AutoField()
    longtip = TextField(null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")])
    shorttip = TextField(null=True)
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_customfilter_filter"


class CustomfilterRule(BaseModel):
    code = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField(null=True)
    enabled = IntegerField(constraints=[SQL("DEFAULT 1")])
    fid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    matches = IntegerField(constraints=[SQL("DEFAULT 1")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    pattern = TextField(null=True)
    prid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    replacement = TextField(null=True)
    rid = AutoField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_customfilter_rule"


class DateFormatLocale(BaseModel):
    format = CharField()
    language = CharField()
    type = CharField()

    class Meta:
        table_name = "moov_date_format_locale"
        indexes = ((("type", "language"), True),)
        primary_key = CompositeKey("language", "type")


class DateFormatType(BaseModel):
    locked = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(index=True)
    type = CharField(primary_key=True)

    class Meta:
        table_name = "moov_date_format_type"


class DateFormats(BaseModel):
    dfid = AutoField()
    format = CharField()
    locked = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField()

    class Meta:
        table_name = "moov_date_formats"
        indexes = ((("format", "type"), True),)


class DdblockBlock(BaseModel):
    delta = AutoField()
    delta_original = CharField(constraints=[SQL("DEFAULT '0'")])
    enabled = IntegerField(constraints=[SQL("DEFAULT 0")])
    module = CharField(constraints=[SQL("DEFAULT ''")])
    title = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_ddblock_block"


class EntityRuleSetting(BaseModel):
    args = TextField(null=True)
    bundle = CharField()
    entity_type = CharField()
    false_msg = CharField(null=True)
    module = CharField(null=True)
    op = CharField()
    rules_config = CharField()
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_entity_rule_setting"
        indexes = (
            (("entity_type", "bundle", "op", "rules_config", "weight"), True),
        )


class Entityform(BaseModel):
    changed = IntegerField(constraints=[SQL("DEFAULT 0")])
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    draft = IntegerField(constraints=[SQL("DEFAULT 0")])
    entityform_id = AutoField()
    language = CharField(constraints=[SQL("DEFAULT ''")])
    type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    uid = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_entityform"


class EntityformType(BaseModel):
    data = TextField(null=True)
    label = CharField(constraints=[SQL("DEFAULT ''")])
    module = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    type = CharField(unique=True)
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_entityform_type"


class EntitylistLists(BaseModel):
    content_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField()
    handler_config = TextField()
    handler_plugin = CharField()
    lid = IntegerField()
    name = CharField()
    title = CharField()

    class Meta:
        table_name = "moov_entitylist_lists"
        indexes = ((("lid", "name"), True),)
        primary_key = CompositeKey("lid", "name")


class EventColors(BaseModel):
    color = TextField()
    module = CharField(constraints=[SQL("DEFAULT 'colors'")])
    selector = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)

    class Meta:
        table_name = "moov_event_colors"


class FeedImportHashes(BaseModel):
    entity = CharField()
    entity_id = IntegerField()
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    feed_group = CharField()
    feed_machine_name = CharField()
    hash = CharField()

    class Meta:
        table_name = "moov_feed_import_hashes"
        indexes = ((("feed_group", "entity", "hash"), False),)


class FeedImportSettings(BaseModel):
    cron_import = IntegerField()
    entity = CharField()
    last_run = IntegerField(constraints=[SQL("DEFAULT 0")])
    last_run_duration = IntegerField(constraints=[SQL("DEFAULT 0")])
    last_run_items = IntegerField(constraints=[SQL("DEFAULT 0")])
    machine_name = CharField(unique=True)
    name = CharField()
    settings = TextField()

    class Meta:
        table_name = "moov_feed_import_settings"


class FeedsImporter(BaseModel):
    config = TextField(null=True)
    id = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)

    class Meta:
        table_name = "moov_feeds_importer"


class FeedsItem(BaseModel):
    entity_id = IntegerField()
    entity_type = CharField(constraints=[SQL("DEFAULT ''")])
    feed_nid = IntegerField(index=True)
    guid = TextField()
    hash = CharField(constraints=[SQL("DEFAULT ''")])
    id = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    imported = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    url = TextField()

    class Meta:
        table_name = "moov_feeds_item"
        indexes = (
            (("entity_type", "entity_id"), True),
            (("entity_type", "guid"), False),
            (("entity_type", "id", "feed_nid", "guid"), False),
            (("entity_type", "id", "feed_nid", "url"), False),
            (("entity_type", "url"), False),
        )
        primary_key = CompositeKey("entity_id", "entity_type")


class FeedsLog(BaseModel):
    feed_nid = IntegerField()
    flid = AutoField()
    id = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    log_time = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    message = TextField()
    request_time = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    severity = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    variables = TextField()

    class Meta:
        table_name = "moov_feeds_log"
        indexes = ((("id", "feed_nid"), False),)


class FeedsPushSubscriptions(BaseModel):
    domain = CharField(constraints=[SQL("DEFAULT ''")])
    hub = TextField()
    post_fields = TextField(null=True)
    secret = CharField(constraints=[SQL("DEFAULT ''")])
    status = CharField(constraints=[SQL("DEFAULT ''")])
    subscriber_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    topic = TextField()

    class Meta:
        table_name = "moov_feeds_push_subscriptions"
        indexes = ((("domain", "subscriber_id"), True),)
        primary_key = CompositeKey("domain", "subscriber_id")


class FeedsSource(BaseModel):
    config = TextField(null=True)
    feed_nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    fetcher_result = TextField(null=True)
    id = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    imported = IntegerField(constraints=[SQL("DEFAULT 0")])
    source = TextField()
    state = TextField(null=True)

    class Meta:
        table_name = "moov_feeds_source"
        indexes = (
            (("id", "feed_nid"), True),
            (("id", "source"), False),
        )
        primary_key = CompositeKey("feed_nid", "id")


class FeedsTamper(BaseModel):
    description = CharField(constraints=[SQL("DEFAULT ''")])
    id = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    importer = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    plugin_id = CharField(constraints=[SQL("DEFAULT ''")])
    settings = TextField(null=True)
    source = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField()

    class Meta:
        table_name = "moov_feeds_tamper"


class FieldCollectionItem(BaseModel):
    archived = IntegerField(constraints=[SQL("DEFAULT 0")])
    field_name = CharField()
    item_id = AutoField()
    revision_id = IntegerField()

    class Meta:
        table_name = "moov_field_collection_item"


class FieldCollectionItemRevision(BaseModel):
    item_id = IntegerField(index=True)
    revision_id = AutoField()

    class Meta:
        table_name = "moov_field_collection_item_revision"


class FieldConfig(BaseModel):
    active = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    cardinality = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField()
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    field_name = CharField(index=True)
    locked = IntegerField(constraints=[SQL("DEFAULT 0")])
    module = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    storage_active = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    storage_module = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    storage_type = CharField(index=True)
    translatable = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(index=True)

    class Meta:
        table_name = "moov_field_config"


class FieldConfigInstance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")])
    data = TextField()
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")])
    field_id = IntegerField()
    field_name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_field_config_instance"
        indexes = ((("field_name", "entity_type", "bundle"), False),)


class FieldDataAdvpollBehavior(BaseModel):
    advpoll_behavior_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_behavior"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollChoice(BaseModel):
    advpoll_choice_choice = CharField()
    advpoll_choice_choice_id = CharField()
    advpoll_choice_write_in = IntegerField(constraints=[SQL("DEFAULT 0")])
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_choice"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollClosed(BaseModel):
    advpoll_closed_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_closed"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollCookieDuration(BaseModel):
    advpoll_cookie_duration_value = IntegerField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_cookie_duration"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollDates(BaseModel):
    advpoll_dates_value = DateTimeField(null=True)
    advpoll_dates_value2 = DateTimeField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_dates"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollMaxChoices(BaseModel):
    advpoll_max_choices_value = IntegerField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_max_choices"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollMode(BaseModel):
    advpoll_mode_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_mode"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollOptions(BaseModel):
    advpoll_options_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_options"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataAdvpollResults(BaseModel):
    advpoll_results_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_advpoll_results"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataBody(BaseModel):
    body_format = CharField(index=True, null=True)
    body_summary = TextField(null=True)
    body_value = TextField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_body"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataCommentBody(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    comment_body_format = CharField(index=True, null=True)
    comment_body_value = TextField(null=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_comment_body"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataEventCalendarDate(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    event_calendar_date_value = DateTimeField(null=True)
    event_calendar_date_value2 = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_event_calendar_date"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataEventCalendarStatus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    event_calendar_status_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_event_calendar_status"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldAdressePharmacieGarde(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_adresse_pharmacie_garde_format = CharField(index=True, null=True)
    field_adresse_pharmacie_garde_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_adresse_pharmacie_garde"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldAfficherDansLaPageDAc(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_afficher_dans_la_page_d_ac_value = IntegerField(
        index=True, null=True
    )
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_afficher_dans_la_page_d_ac"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldAfficherDansLeSlider(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_afficher_dans_le_slider_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_afficher_dans_le_slider"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldArrivee(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_arrivee_format = CharField(index=True, null=True)
    field_arrivee_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_arrivee"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldArriveeDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_arrivee_du_vol_format = CharField(index=True, null=True)
    field_arrivee_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_arrivee_du_vol"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldAuteur(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_auteur_format = CharField(index=True, null=True)
    field_auteur_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_auteur"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldAutreTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_autre_t_l_phone_revision_id = IntegerField(index=True, null=True)
    field_autre_t_l_phone_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_autre_t_l_phone"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCatGorieDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_cat_gorie_de_l_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_cat_gorie_de_l_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCatGorieSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_cat_gorie_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_cat_gorie_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCategorieDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_de_l_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_categorie_de_l_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCategorieForum(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_forum_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_categorie_forum"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCategorieLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_live_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_categorie_live"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCategorieNumeroUrgence(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_numero_urgence_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_categorie_numero_urgence"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldChaNeTv(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_cha_ne_tv_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_cha_ne_tv"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldChannelId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_channel_id_format = CharField(index=True, null=True)
    field_channel_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_channel_id"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldChapeau(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_chapeau_format = CharField(index=True, null=True)
    field_chapeau_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_chapeau"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldChoisirCommeContact(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_choisir_comme_contact_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_choisir_comme_contact"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldChoixTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_choix_t_l_phone_revision_id = IntegerField(index=True, null=True)
    field_choix_t_l_phone_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_choix_t_l_phone"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldClouds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_clouds_format = CharField(index=True, null=True)
    field_clouds_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_clouds"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCodeProvince(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_code_province_format = CharField(index=True, null=True)
    field_code_province_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_code_province"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCodeRegion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_code_region_format = CharField(index=True, null=True)
    field_code_region_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_code_region"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCompagnieDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_compagnie_du_vol_format = CharField(index=True, null=True)
    field_compagnie_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_compagnie_du_vol"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCompteurAccueil(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_compteur_accueil_value = IntegerField(constraints=[SQL("DEFAULT 1")])
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_compteur_accueil"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCompteurCategorie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_compteur_categorie_value = CharField(
        constraints=[SQL("DEFAULT '1'")], null=True
    )
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_compteur_categorie"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldConditionDeVente(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_condition_de_vente_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_condition_de_vente"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldConditionDeVenteAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_condition_de_vente_annonce_format = CharField(index=True, null=True)
    field_condition_de_vente_annonce_summary = TextField(null=True)
    field_condition_de_vente_annonce_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_condition_de_vente_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldConditionDeVentePublici(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_condition_de_vente_publici_value = IntegerField(
        index=True, null=True
    )
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_condition_de_vente_publici"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldContact(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_contact"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldContactDesJournalistes(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_des_journalistes_format = CharField(index=True, null=True)
    field_contact_des_journalistes_summary = TextField(null=True)
    field_contact_des_journalistes_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_contact_des_journalistes"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldContactMe(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_me_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_contact_me"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldContactRapide(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_rapide__format = CharField(index=True, null=True)
    field_contact_rapide__value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_contact_rapide_"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldContactRapideAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_rapide_ads_format = CharField(index=True, null=True)
    field_contact_rapide_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_contact_rapide_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldContenuArticle(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contenu_article_format = CharField(index=True, null=True)
    field_contenu_article_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_contenu_article"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightContenu(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_contenu"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightContenuDecouvri(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_decouvri_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_contenu_decouvri"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightContenuEducatio(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_educatio_format = CharField(index=True, null=True)
    field_copyright_contenu_educatio_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_contenu_educatio"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightContenuTendace(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_tendace_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_contenu_tendace"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightImageActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_actus_format = CharField(index=True, null=True)
    field_copyright_image_actus_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_image_actus"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightImageDecouvrir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_decouvrir_format = CharField(index=True, null=True)
    field_copyright_image_decouvrir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_image_decouvrir"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightImageEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_education_format = CharField(index=True, null=True)
    field_copyright_image_education_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_image_education"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightImageGallery(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_gallery_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_image_gallery"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCopyrightImageTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_tendance_format = CharField(index=True, null=True)
    field_copyright_image_tendance_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_copyright_image_tendance"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCourriel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_courriel_format = CharField(index=True, null=True)
    field_courriel_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_courriel"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCourse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_course_format = CharField(index=True, null=True)
    field_course_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_course"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldCouvertureOuiNon(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_couverture_oui_non_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_couverture_oui_non"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDPartDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_d_part_du_vol_format = CharField(index=True, null=True)
    field_d_part_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_d_part_du_vol"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDArrivE(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_d_arriv_e_format = CharField(index=True, null=True)
    field_date_d_arriv_e_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_d_arriv_e"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDeDButDiffusion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_d_but_diffusion_value = DateTimeField(null=True)
    field_date_de_d_but_diffusion_value2 = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_de_d_but_diffusion"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDeDiffusionAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_diffusion_ads_value = CharField(null=True)
    field_date_de_diffusion_ads_value2 = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_de_diffusion_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDeFinPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_fin_publicite_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_de_fin_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDePublication(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_publication_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_de_publication"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDebutDiffusion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_debut_diffusion_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_debut_diffusion"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDebutPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_debut_publicite_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_debut_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDuCours(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_cours_format = CharField(index=True, null=True)
    field_date_du_cours_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_du_cours"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDuCourse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_course_format = CharField(index=True, null=True)
    field_date_du_course_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_du_course"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDuProgramme(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_programme_format = CharField(index=True, null=True)
    field_date_du_programme_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_du_programme"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_vol_format = CharField(index=True, null=True)
    field_date_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_du_vol"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateEndAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_end_annonce_format = CharField(index=True, null=True)
    field_date_end_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_end_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateEndPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_end_publicite_format = CharField(index=True, null=True)
    field_date_end_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_end_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateEvenement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_evenement_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_evenement"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateFinDiffusion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_fin_diffusion_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_fin_diffusion"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateMeteo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_meteo_format = CharField(index=True, null=True)
    field_date_meteo_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_meteo"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDatePartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_partenaire_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_partenaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDatePublicationAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_publication_annonce_format = CharField(index=True, null=True)
    field_date_publication_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_publication_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDatePublicationPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_publication_publicite_format = CharField(index=True, null=True)
    field_date_publication_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_publication_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_small_ads_value = CharField(null=True)
    field_date_small_ads_value2 = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateStartAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_start_annonce_format = CharField(index=True, null=True)
    field_date_start_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_start_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDateStartPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_start_publicite_format = CharField(index=True, null=True)
    field_date_start_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_date_start_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionActualite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_actualite_format = CharField(index=True, null=True)
    field_description_actualite_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_actualite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_de_l_annonce_format = CharField(index=True, null=True)
    field_description_de_l_annonce_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_de_l_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionDecouvrirMada(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_decouvrir_mada_format = CharField(index=True, null=True)
    field_description_decouvrir_mada_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_decouvrir_mada"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionECommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_e_commerce_format = CharField(index=True, null=True)
    field_description_e_commerce_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_e_commerce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_education_format = CharField(index=True, null=True)
    field_description_education_summary = TextField(null=True)
    field_description_education_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_education"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionEvenement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_evenement_format = CharField(index=True, null=True)
    field_description_evenement_summary = TextField(null=True)
    field_description_evenement_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_evenement"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionFilDinfo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_fil_dinfo_format = CharField(index=True, null=True)
    field_description_fil_dinfo_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_fil_dinfo"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionHotel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_hotel_format = CharField(index=True, null=True)
    field_description_hotel_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_hotel"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_partenaire_format = CharField(index=True, null=True)
    field_description_partenaire_summary = TextField(null=True)
    field_description_partenaire_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_partenaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_small_ads_format = CharField(index=True, null=True)
    field_description_small_ads_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_tendance_format = CharField(index=True, null=True)
    field_description_tendance_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_tendance"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDescriptionUtilisateur(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_utilisateur_format = CharField(index=True, null=True)
    field_description_utilisateur_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_description_utilisateur"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDestination(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_destination_format = CharField(index=True, null=True)
    field_destination_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_destination"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldDevise(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_devise_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_devise"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldEMailProfessionnel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_e_mail_professionnel_format = CharField(index=True, null=True)
    field_e_mail_professionnel_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_e_mail_professionnel"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldEmailProfessionnelAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_email_professionnel_ads_format = CharField(index=True, null=True)
    field_email_professionnel_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_email_professionnel_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldEmplacement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_emplacement"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldEmplacementDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_de_l_annonce_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_emplacement_de_l_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldEmplacementDisponiblePub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_disponible_pub_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_emplacement_disponible_pub"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldEmplacementDuPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_du_pub_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_emplacement_du_pub_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldFeedItemDescription(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_feed_item_description_format = CharField(index=True, null=True)
    field_feed_item_description_summary = TextField(null=True)
    field_feed_item_description_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_feed_item_description"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldFluxRssConnectedLife(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_connected_life_format = CharField(index=True, null=True)
    field_flux_rss_connected_life_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_flux_rss_connected_life"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldFluxRssInternationale(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_internationale_format = CharField(index=True, null=True)
    field_flux_rss_internationale_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_flux_rss_internationale"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldFluxRssMedecineEtSante(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_medecine_et_sante_format = CharField(index=True, null=True)
    field_flux_rss_medecine_et_sante_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_flux_rss_medecine_et_sante"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldFluxRssPeople(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_people_format = CharField(index=True, null=True)
    field_flux_rss_people_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_flux_rss_people"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldFormatDuPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_format_du_pub_format = CharField(index=True, null=True)
    field_format_du_pub_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_format_du_pub"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldFormatDuPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_format_du_pub_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_format_du_pub_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldGrilleTarifaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_grille_tarifaire_format = CharField(null=True)
    field_grille_tarifaire_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_grille_tarifaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldGrilleTarifairePublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_grille_tarifaire_publicite_format = CharField(null=True)
    field_grille_tarifaire_publicite_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_grille_tarifaire_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldGuideAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_guide_annonce_format = CharField(index=True, null=True)
    field_guide_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_guide_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldHeureArrivE(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_arriv_e_format = CharField(index=True, null=True)
    field_heure_arriv_e_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_heure_arriv_e"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldHeureDPart(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_d_part_format = CharField(index=True, null=True)
    field_heure_d_part_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_heure_d_part"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldHeureDuProgramme(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_du_programme_format = CharField(index=True, null=True)
    field_heure_du_programme_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_heure_du_programme"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldHeureSortir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_sortir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_heure_sortir"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldHomepage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_homepage_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_homepage"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldHumidite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_humidite_format = CharField(index=True, null=True)
    field_humidite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_humidite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldIcone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_alt = CharField(null=True)
    field_icone_fid = IntegerField(index=True, null=True)
    field_icone_height = IntegerField(null=True)
    field_icone_title = CharField(null=True)
    field_icone_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_icone"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldIconeActualites(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_actualites_format = CharField(index=True, null=True)
    field_icone_actualites_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_icone_actualites"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldIconeDCouvrirMCar(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_d_couvrir_m_car_format = CharField(index=True, null=True)
    field_icone_d_couvrir_m_car_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_icone_d_couvrir_m_car"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldIconeTendanceMoov(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_tendance_moov_format = CharField(index=True, null=True)
    field_icone_tendance_moov_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_icone_tendance_moov"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_id_format = CharField(index=True, null=True)
    field_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_id"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_alt = CharField(null=True)
    field_image_fid = IntegerField(index=True, null=True)
    field_image_height = IntegerField(null=True)
    field_image_title = CharField(null=True)
    field_image_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_actus_alt = CharField(null=True)
    field_image_actus_fid = IntegerField(index=True, null=True)
    field_image_actus_height = IntegerField(null=True)
    field_image_actus_title = CharField(null=True)
    field_image_actus_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_actus"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageAnnonceDefault(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_annonce_default_alt = CharField(null=True)
    field_image_annonce_default_fid = IntegerField(index=True, null=True)
    field_image_annonce_default_height = IntegerField(null=True)
    field_image_annonce_default_title = CharField(null=True)
    field_image_annonce_default_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_annonce_default"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageDeCouvertureLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_couverture_live_alt = CharField(null=True)
    field_image_de_couverture_live_fid = IntegerField(index=True, null=True)
    field_image_de_couverture_live_height = IntegerField(null=True)
    field_image_de_couverture_live_title = CharField(null=True)
    field_image_de_couverture_live_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_de_couverture_live"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_l_annonce_alt = CharField(null=True)
    field_image_de_l_annonce_fid = IntegerField(index=True, null=True)
    field_image_de_l_annonce_height = IntegerField(null=True)
    field_image_de_l_annonce_title = CharField(null=True)
    field_image_de_l_annonce_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_de_l_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageDeLaPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_la_pub_alt = CharField(null=True)
    field_image_de_la_pub_fid = IntegerField(index=True, null=True)
    field_image_de_la_pub_height = IntegerField(null=True)
    field_image_de_la_pub_title = CharField(null=True)
    field_image_de_la_pub_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_de_la_pub"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageDeLaPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_la_pub_ads_alt = CharField(null=True)
    field_image_de_la_pub_ads_fid = IntegerField(index=True, null=True)
    field_image_de_la_pub_ads_height = IntegerField(null=True)
    field_image_de_la_pub_ads_title = CharField(null=True)
    field_image_de_la_pub_ads_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_de_la_pub_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageECommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_e_commerce_alt = CharField(null=True)
    field_image_e_commerce_fid = IntegerField(index=True, null=True)
    field_image_e_commerce_height = IntegerField(null=True)
    field_image_e_commerce_title = CharField(null=True)
    field_image_e_commerce_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_e_commerce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_education_alt = CharField(null=True)
    field_image_education_fid = IntegerField(index=True, null=True)
    field_image_education_height = IntegerField(null=True)
    field_image_education_title = CharField(null=True)
    field_image_education_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_education"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageEvent(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_event_alt = CharField(null=True)
    field_image_event_fid = IntegerField(index=True, null=True)
    field_image_event_height = IntegerField(null=True)
    field_image_event_title = CharField(null=True)
    field_image_event_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_event"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageGuide(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_guide_alt = CharField(null=True)
    field_image_guide_fid = IntegerField(index=True, null=True)
    field_image_guide_height = IntegerField(null=True)
    field_image_guide_title = CharField(null=True)
    field_image_guide_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_guide"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageLogo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_logo_alt = CharField(null=True)
    field_image_logo_fid = IntegerField(index=True, null=True)
    field_image_logo_height = IntegerField(null=True)
    field_image_logo_title = CharField(null=True)
    field_image_logo_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_logo"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageParDefautAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_par_defaut_annonce_alt = CharField(null=True)
    field_image_par_defaut_annonce_fid = IntegerField(index=True, null=True)
    field_image_par_defaut_annonce_height = IntegerField(null=True)
    field_image_par_defaut_annonce_title = CharField(null=True)
    field_image_par_defaut_annonce_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_par_defaut_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagePopin(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_popin_alt = CharField(null=True)
    field_image_popin_fid = IntegerField(index=True, null=True)
    field_image_popin_height = IntegerField(null=True)
    field_image_popin_title = CharField(null=True)
    field_image_popin_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_popin"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagePubFooter(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_pub_footer_alt = CharField(null=True)
    field_image_pub_footer_class = CharField(null=True)
    field_image_pub_footer_fid = IntegerField(index=True, null=True)
    field_image_pub_footer_height = IntegerField(null=True)
    field_image_pub_footer_longdesc = CharField(null=True)
    field_image_pub_footer_rel = CharField(null=True)
    field_image_pub_footer_target = CharField(null=True)
    field_image_pub_footer_title = CharField(null=True)
    field_image_pub_footer_url = CharField(null=True)
    field_image_pub_footer_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_pub_footer"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagePubHautPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_pub_haut_pub_alt = CharField(null=True)
    field_image_pub_haut_pub_class = CharField(null=True)
    field_image_pub_haut_pub_fid = IntegerField(index=True, null=True)
    field_image_pub_haut_pub_height = IntegerField(null=True)
    field_image_pub_haut_pub_longdesc = CharField(null=True)
    field_image_pub_haut_pub_rel = CharField(null=True)
    field_image_pub_haut_pub_target = CharField(null=True)
    field_image_pub_haut_pub_title = CharField(null=True)
    field_image_pub_haut_pub_url = CharField(null=True)
    field_image_pub_haut_pub_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_pub_haut_pub"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_small_ads_alt = CharField(null=True)
    field_image_small_ads_fid = IntegerField(index=True, null=True)
    field_image_small_ads_height = IntegerField(null=True)
    field_image_small_ads_title = CharField(null=True)
    field_image_small_ads_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageVolutionDuDevise(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_volution_du_devise_alt = CharField(null=True)
    field_image_volution_du_devise_fid = IntegerField(index=True, null=True)
    field_image_volution_du_devise_height = IntegerField(null=True)
    field_image_volution_du_devise_title = CharField(null=True)
    field_image_volution_du_devise_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_volution_du_devise"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageVotrePubSurMoov(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_votre_pub_sur_moov_alt = CharField(null=True)
    field_image_votre_pub_sur_moov_fid = IntegerField(index=True, null=True)
    field_image_votre_pub_sur_moov_height = IntegerField(null=True)
    field_image_votre_pub_sur_moov_title = CharField(null=True)
    field_image_votre_pub_sur_moov_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_image_votre_pub_sur_moov"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImages(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_revision_id = IntegerField(index=True, null=True)
    field_images_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_images"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagesActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_actus_revision_id = IntegerField(index=True, null=True)
    field_images_actus_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_images_actus"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagesFondPublicitaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_fond_publicitaire_alt = CharField(null=True)
    field_images_fond_publicitaire_fid = IntegerField(index=True, null=True)
    field_images_fond_publicitaire_height = IntegerField(null=True)
    field_images_fond_publicitaire_title = CharField(null=True)
    field_images_fond_publicitaire_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_images_fond_publicitaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagesLookDuJour(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_look_du_jour_alt = CharField(null=True)
    field_images_look_du_jour_fid = IntegerField(index=True, null=True)
    field_images_look_du_jour_height = IntegerField(null=True)
    field_images_look_du_jour_title = CharField(null=True)
    field_images_look_du_jour_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_images_look_du_jour"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagesPubBas(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_pub_bas_alt = CharField(null=True)
    field_images_pub_bas_class = CharField(null=True)
    field_images_pub_bas_fid = IntegerField(index=True, null=True)
    field_images_pub_bas_height = IntegerField(null=True)
    field_images_pub_bas_longdesc = CharField(null=True)
    field_images_pub_bas_rel = CharField(null=True)
    field_images_pub_bas_target = CharField(null=True)
    field_images_pub_bas_title = CharField(null=True)
    field_images_pub_bas_url = CharField(null=True)
    field_images_pub_bas_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_images_pub_bas"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagesPubCarrebas(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_pub_carrebas_alt = CharField(null=True)
    field_images_pub_carrebas_class = CharField(null=True)
    field_images_pub_carrebas_fid = IntegerField(index=True, null=True)
    field_images_pub_carrebas_height = IntegerField(null=True)
    field_images_pub_carrebas_longdesc = CharField(null=True)
    field_images_pub_carrebas_rel = CharField(null=True)
    field_images_pub_carrebas_target = CharField(null=True)
    field_images_pub_carrebas_title = CharField(null=True)
    field_images_pub_carrebas_url = CharField(null=True)
    field_images_pub_carrebas_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_images_pub_carrebas"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImagesPubCarrehaut(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_pub_carrehaut_alt = CharField(null=True)
    field_images_pub_carrehaut_class = CharField(null=True)
    field_images_pub_carrehaut_fid = IntegerField(index=True, null=True)
    field_images_pub_carrehaut_height = IntegerField(null=True)
    field_images_pub_carrehaut_longdesc = CharField(null=True)
    field_images_pub_carrehaut_rel = CharField(null=True)
    field_images_pub_carrehaut_target = CharField(null=True)
    field_images_pub_carrehaut_title = CharField(null=True)
    field_images_pub_carrehaut_url = CharField(null=True)
    field_images_pub_carrehaut_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_images_pub_carrehaut"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldImageschamps(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_imageschamps_alt = CharField(null=True)
    field_imageschamps_fid = IntegerField(index=True, null=True)
    field_imageschamps_height = IntegerField(null=True)
    field_imageschamps_title = CharField(null=True)
    field_imageschamps_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_imageschamps"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLibelle(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_libelle_format = CharField(index=True, null=True)
    field_libelle_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_libelle"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienDuPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_du_partenaire_format = CharField(index=True, null=True)
    field_lien_du_partenaire_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_du_partenaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienHotel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_hotel_format = CharField(index=True, null=True)
    field_lien_hotel_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_hotel"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienImage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_image_format = CharField(index=True, null=True)
    field_lien_image_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_image"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienImagePublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_image_publicite_format = CharField(index=True, null=True)
    field_lien_image_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_image_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_live_format = CharField(index=True, null=True)
    field_lien_live_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_live"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienSortir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sortir_format = CharField(index=True, null=True)
    field_lien_sortir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_sortir"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienSponsorisActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_actus_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_sponsoris_actus"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienSponsorisDecouvrir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_decouvrir_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_sponsoris_decouvrir"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienSponsorisEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_education_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_sponsoris_education"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienSponsorisTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_tendance_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_sponsoris_tendance"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLienVotrePubSurMoov(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_votre_pub_sur_moov_format = CharField(index=True, null=True)
    field_lien_votre_pub_sur_moov_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lien_votre_pub_sur_moov"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLieuAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lieu_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLieuEntityform(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_entityform_format = CharField(index=True, null=True)
    field_lieu_entityform_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lieu_entityform"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLieuEvenement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_evenement_format = CharField(index=True, null=True)
    field_lieu_evenement_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lieu_evenement"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLieuPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_partenaire_format = CharField(index=True, null=True)
    field_lieu_partenaire_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lieu_partenaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLieuSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_lieu_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldListesDesProvinces(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_listes_des_provinces_format = CharField(index=True, null=True)
    field_listes_des_provinces_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_listes_des_provinces"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLogoCopyright(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_alt = CharField(null=True)
    field_logo_copyright_fid = IntegerField(index=True, null=True)
    field_logo_copyright_height = IntegerField(null=True)
    field_logo_copyright_title = CharField(null=True)
    field_logo_copyright_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_logo_copyright"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLogoCopyrightDecouvrir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_decouvrir_alt = CharField(null=True)
    field_logo_copyright_decouvrir_fid = IntegerField(index=True, null=True)
    field_logo_copyright_decouvrir_height = IntegerField(null=True)
    field_logo_copyright_decouvrir_title = CharField(null=True)
    field_logo_copyright_decouvrir_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_logo_copyright_decouvrir"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLogoCopyrightEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_education_alt = CharField(null=True)
    field_logo_copyright_education_fid = IntegerField(index=True, null=True)
    field_logo_copyright_education_height = IntegerField(null=True)
    field_logo_copyright_education_title = CharField(null=True)
    field_logo_copyright_education_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_logo_copyright_education"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLogoCopyrightTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_tendance_alt = CharField(null=True)
    field_logo_copyright_tendance_fid = IntegerField(index=True, null=True)
    field_logo_copyright_tendance_height = IntegerField(null=True)
    field_logo_copyright_tendance_title = CharField(null=True)
    field_logo_copyright_tendance_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_logo_copyright_tendance"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLogoLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_live_alt = CharField(null=True)
    field_logo_live_fid = IntegerField(index=True, null=True)
    field_logo_live_height = IntegerField(null=True)
    field_logo_live_title = CharField(null=True)
    field_logo_live_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_logo_live"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLogoMedia(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_media_alt = CharField(null=True)
    field_logo_media_fid = IntegerField(index=True, null=True)
    field_logo_media_height = IntegerField(null=True)
    field_logo_media_title = CharField(null=True)
    field_logo_media_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_logo_media"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldLogoPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_partenaire_alt = CharField(null=True)
    field_logo_partenaire_fid = IntegerField(index=True, null=True)
    field_logo_partenaire_height = IntegerField(null=True)
    field_logo_partenaire_title = CharField(null=True)
    field_logo_partenaire_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_logo_partenaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMeteo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_meteo_format = CharField(index=True, null=True)
    field_meteo_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_meteo"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMeteoweek(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_meteoweek_format = CharField(index=True, null=True)
    field_meteoweek_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_meteoweek"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMettreEnCouverture(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_mettre_en_couverture_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_mettre_en_couverture"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldModRationCondition(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_mod_ration_condition_format = CharField(index=True, null=True)
    field_mod_ration_condition_summary = TextField(null=True)
    field_mod_ration_condition_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_mod_ration_condition"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMontantDeLaPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_de_la_publicite_format = CharField(index=True, null=True)
    field_montant_de_la_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_montant_de_la_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMontantEnAriary(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_en_ariary_format = CharField(index=True, null=True)
    field_montant_en_ariary_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_montant_en_ariary"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMontantPayer(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_payer_format = CharField(index=True, null=True)
    field_montant_payer_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_montant_payer"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMontantPayerSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_payer_small_ads_format = CharField(index=True, null=True)
    field_montant_payer_small_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_montant_payer_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMontantPubliciteAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_publicite_ads_format = CharField(index=True, null=True)
    field_montant_publicite_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_montant_publicite_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldMvolaPharmacie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_mvola_pharmacie_format = CharField(index=True, null=True)
    field_mvola_pharmacie_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_mvola_pharmacie"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNom(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_format = CharField(index=True, null=True)
    field_nom_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nom"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNomDeLaSociete(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_de_la_societe_format = CharField(index=True, null=True)
    field_nom_de_la_societe_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nom_de_la_societe"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNomDuPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_du_pub_format = CharField(index=True, null=True)
    field_nom_du_pub_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nom_du_pub"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNomSocieteAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_societe_ads_format = CharField(index=True, null=True)
    field_nom_societe_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nom_societe_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNombreDeJourAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_ads_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nombre_de_jour_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNombreDeJourAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_annonce_format = CharField(index=True, null=True)
    field_nombre_de_jour_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nombre_de_jour_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNombreDeJourPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_publicite_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nombre_de_jour_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNombreDeJourSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_small_ads_format = CharField(index=True, null=True)
    field_nombre_de_jour_small_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nombre_de_jour_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNombreDeTransaction(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_transaction_format = CharField(index=True, null=True)
    field_nombre_de_transaction_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nombre_de_transaction"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNomicone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nomicone_format = CharField(index=True, null=True)
    field_nomicone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_nomicone"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNumero(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_format = CharField(index=True, null=True)
    field_numero_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_numero"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNumeroDeLaPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_de_la_pub_ads_format = CharField(index=True, null=True)
    field_numero_de_la_pub_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_numero_de_la_pub_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNumeroDeTelephone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_de_telephone_format = CharField(index=True, null=True)
    field_numero_de_telephone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_numero_de_telephone"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNumeroDeTelephoneAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_de_telephone_ads_format = CharField(index=True, null=True)
    field_numero_de_telephone_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_numero_de_telephone_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNumeroTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_t_l_phone_format = CharField(index=True, null=True)
    field_numero_t_l_phone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_numero_t_l_phone"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldNumeroTphAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_tph_annonce_format = CharField(index=True, null=True)
    field_numero_tph_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_numero_tph_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldOrigine(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_origine_format = CharField(index=True, null=True)
    field_origine_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_origine"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPageDeLaPubliciteAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_page_de_la_publicite_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_page_de_la_publicite_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPetitesAnnoncesId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_petites_annonces_id_format = CharField(index=True, null=True)
    field_petites_annonces_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_petites_annonces_id"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPhoneNumber(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_phone_number_format = CharField(index=True, null=True)
    field_phone_number_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_phone_number"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPrNoms(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_pr_noms_format = CharField(index=True, null=True)
    field_pr_noms_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_pr_noms"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPressure(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_pressure_format = CharField(index=True, null=True)
    field_pressure_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_pressure"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPrice(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_price_format = CharField(index=True, null=True)
    field_price_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_price"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPrixEnAriary(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_prix_en_ariary_value = FloatField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_prix_en_ariary"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldPubliciteId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_publicite_id_format = CharField(index=True, null=True)
    field_publicite_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_publicite_id"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuartBnous4Rapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_bnous_4_rapport_format = CharField(index=True, null=True)
    field_quart_bnous_4_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quart_bnous_4_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuartBonus4Isa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_bonus_4_isa_format = CharField(index=True, null=True)
    field_quart_bonus_4_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quart_bonus_4_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuartDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_desordre_isa_format = CharField(index=True, null=True)
    field_quart_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quart_desordre_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuartDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_desordre_rapport_format = CharField(index=True, null=True)
    field_quart_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quart_desordre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuartOrdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_ordre_rapport_format = CharField(index=True, null=True)
    field_quart_ordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quart_ordre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuarteOrdreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quarte_ordre_isa_format = CharField(index=True, null=True)
    field_quarte_ordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quarte_ordre_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuintBonusIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_bonus_isa_format = CharField(index=True, null=True)
    field_quint_bonus_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quint_bonus_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuintBonusRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_bonus_rapport_format = CharField(index=True, null=True)
    field_quint_bonus_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quint_bonus_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuintDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_desordre_isa_format = CharField(index=True, null=True)
    field_quint_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quint_desordre_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuintDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_desordre_rapport_format = CharField(index=True, null=True)
    field_quint_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quint_desordre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuintOrdreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_ordre_isa_format = CharField(index=True, null=True)
    field_quint_ordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quint_ordre_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldQuintOrdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_ordre_rapport_format = CharField(index=True, null=True)
    field_quint_ordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_quint_ordre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldRFRenceDePaiementMvol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_r_f_rence_de_paiement_mvol_format = CharField(index=True, null=True)
    field_r_f_rence_de_paiement_mvol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_r_f_rence_de_paiement_mvol"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldRFRencePaiementMvola(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_r_f_rence_paiement_mvola_format = CharField(index=True, null=True)
    field_r_f_rence_paiement_mvola_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_r_f_rence_paiement_mvola"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldRGionPharmacieListe(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_r_gion_pharmacie_liste_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_r_gion_pharmacie_liste"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldReferenceMvola(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_reference_mvola_format = CharField(index=True, null=True)
    field_reference_mvola_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_reference_mvola"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldReferenceMvolaAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_reference_mvola_ads_format = CharField(index=True, null=True)
    field_reference_mvola_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_reference_mvola_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldReponse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_reponse_format = CharField(index=True, null=True)
    field_reponse_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_reponse"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldRestricitonMineurForum(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_restriciton_mineur_forum_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_restriciton_mineur_forum"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldRestrictionMineurCondit(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_restriction_mineur_condit_format = CharField(index=True, null=True)
    field_restriction_mineur_condit_summary = TextField(null=True)
    field_restriction_mineur_condit_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_restriction_mineur_condit"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldRubriqueCategorie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_rubrique_categorie_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_rubrique_categorie"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSaisirNouveauNumero(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_saisir_nouveau_numero_format = CharField(index=True, null=True)
    field_saisir_nouveau_numero_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_saisir_nouveau_numero"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSaisirUnNouveauEmail(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_saisir_un_nouveau_email_email = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_saisir_un_nouveau_email"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSemaineDeGarde(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_semaine_de_garde_format = CharField(index=True, null=True)
    field_semaine_de_garde_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_semaine_de_garde"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSixteBonus4Isa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_bonus_4_isa_format = CharField(index=True, null=True)
    field_sixte_bonus_4_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sixte_bonus_4_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSixteBonus4Rapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_bonus_4_rapport_format = CharField(index=True, null=True)
    field_sixte_bonus_4_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sixte_bonus_4_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSixteDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_desordre_isa_format = CharField(index=True, null=True)
    field_sixte_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sixte_desordre_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSixteDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_desordre_rapport_format = CharField(index=True, null=True)
    field_sixte_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sixte_desordre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSixteOdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_odre_rapport_format = CharField(index=True, null=True)
    field_sixte_odre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sixte_odre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSixteOrdre(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_ordre_format = CharField(index=True, null=True)
    field_sixte_ordre_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sixte_ordre"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSliderPageAccueil(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_slider_page_accueil_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_slider_page_accueil"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSliderPageCategorie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_slider_page_categorie_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_slider_page_categorie"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSliderPageCategorieIn(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_slider_page_categorie_in_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_slider_page_categorie_in"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSourceCours(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_source_cours_format = CharField(index=True, null=True)
    field_source_cours_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_source_cours"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSousCatGorieAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_cat_gorie_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sous_cat_gorie_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSousCategorieSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_categorie_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sous_categorie_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSousTitreEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_titre_education_format = CharField(index=True, null=True)
    field_sous_titre_education_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sous_titre_education"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldSousTitreTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_titre_tendance_format = CharField(index=True, null=True)
    field_sous_titre_tendance_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_sous_titre_tendance"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldStatusDeLaTransaction(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_status_de_la_transaction_format = CharField(index=True, null=True)
    field_status_de_la_transaction_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_status_de_la_transaction"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldStatusTransactionPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_status_transaction_pub_format = CharField(index=True, null=True)
    field_status_transaction_pub_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_status_transaction_pub"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldStatutTransactionAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_statut_transaction_ads_format = CharField(index=True, null=True)
    field_statut_transaction_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_statut_transaction_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_t_l_phone_format = CharField(index=True, null=True)
    field_t_l_phone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_t_l_phone"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTags(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tags_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_tags"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTelephonePharmacie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_telephone_pharmacie_format = CharField(index=True, null=True)
    field_telephone_pharmacie_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_telephone_pharmacie"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTemperatureJour(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_jour_format = CharField(index=True, null=True)
    field_temperature_jour_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_temperature_jour"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTemperatureMatin(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_matin_format = CharField(index=True, null=True)
    field_temperature_matin_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_temperature_matin"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTemperatureMax(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_max_format = CharField(index=True, null=True)
    field_temperature_max_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_temperature_max"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTemperatureNuit(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_nuit_format = CharField(index=True, null=True)
    field_temperature_nuit_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_temperature_nuit"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTemperatureSoir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_soir_format = CharField(index=True, null=True)
    field_temperature_soir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_temperature_soir"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTierceBonusIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_bonus_isa_format = CharField(index=True, null=True)
    field_tierce_bonus_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_tierce_bonus_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTierceDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_desordre_isa_format = CharField(index=True, null=True)
    field_tierce_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_tierce_desordre_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTierceDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_desordre_rapport_format = CharField(index=True, null=True)
    field_tierce_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_tierce_desordre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTierceOrdreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_ordre_isa_format = CharField(index=True, null=True)
    field_tierce_ordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_tierce_ordre_isa"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTierceOrdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_ordre_rapport_format = CharField(index=True, null=True)
    field_tierce_ordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_tierce_ordre_rapport"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTitreAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_titre_annonce_format = CharField(index=True, null=True)
    field_titre_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_titre_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTitreTest(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_titre_test_format = CharField(index=True, null=True)
    field_titre_test_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_titre_test"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTokenId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_token_id_format = CharField(index=True, null=True)
    field_token_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_token_id"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTokenIdAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_token_id_ads_format = CharField(index=True, null=True)
    field_token_id_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_token_id_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTokenIdPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_token_id_publicite_format = CharField(index=True, null=True)
    field_token_id_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_token_id_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTransactionId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_transaction_id_format = CharField(index=True, null=True)
    field_transaction_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_transaction_id"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTransactionIdPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_transaction_id_publicite_format = CharField(index=True, null=True)
    field_transaction_id_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_transaction_id_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeActualite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_actualite_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_actualite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeDeCondition(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_condition_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_de_condition"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeDeMedia(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_media_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_de_media"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeDeVidO(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_vid_o_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_de_vid_o"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeDeVotreAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_votre_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_de_votre_annonce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeDecouvrirMadagascar(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_decouvrir_madagascar_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_decouvrir_madagascar"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeDuProgramme(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_du_programme_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_du_programme"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_du_vol_format = CharField(index=True, null=True)
    field_type_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_du_vol"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeECommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_e_commerce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_e_commerce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_small_ads"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldTypeTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_tendance_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_type_tendance"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlMedia(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_media_format = CharField(index=True, null=True)
    field_url_media_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_media"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPageEcommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_ecommerce_format = CharField(index=True, null=True)
    field_url_page_ecommerce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_ecommerce"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPageEmploi(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_emploi_format = CharField(index=True, null=True)
    field_url_page_emploi_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_emploi"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPageIframe(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_iframe_format = CharField(index=True, null=True)
    field_url_page_iframe_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_iframe"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPagePmu(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_pmu_format = CharField(index=True, null=True)
    field_url_page_pmu_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_pmu"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPagePratiqueReservez(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_pratique_reservez_format = CharField(index=True, null=True)
    field_url_page_pratique_reservez_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_pratique_reservez"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPageRelooking(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_relooking_format = CharField(index=True, null=True)
    field_url_page_relooking_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_relooking"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPageSelfcare(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_selfcare_format = CharField(index=True, null=True)
    field_url_page_selfcare_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_selfcare"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlPageVotrePublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_votre_publicite_format = CharField(index=True, null=True)
    field_url_page_votre_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_page_votre_publicite"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldUrlVidO(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_vid_o_format = CharField(index=True, null=True)
    field_url_vid_o_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_url_vid_o"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVidOEvent(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_vid_o_event_format = CharField(index=True, null=True)
    field_vid_o_event_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_vid_o_event"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVidOStreaming(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_vid_o_streaming_description = TextField(null=True)
    field_vid_o_streaming_display = IntegerField(
        constraints=[SQL("DEFAULT 1")]
    )
    field_vid_o_streaming_fid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_vid_o_streaming"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVideoUrl(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_video_url_format = CharField(index=True, null=True)
    field_video_url_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_video_url"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVideosDuJour(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_videos_du_jour_format = CharField(index=True, null=True)
    field_videos_du_jour_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_videos_du_jour"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVille(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_ville_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_ville"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVillePartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_ville_partenaire_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_ville_partenaire"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVitesse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_vitesse_format = CharField(index=True, null=True)
    field_vitesse_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_vitesse"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVolume(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_volume_format = CharField(index=True, null=True)
    field_volume_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_volume"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldVotrePubDansLaPage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_votre_pub_dans_la_page_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_votre_pub_dans_la_page"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldWeatherCom(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_weather_com_format = CharField(index=True, null=True)
    field_weather_com_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_weather_com"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldWorldWeatherOnline(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_world_weather_online_format = CharField(index=True, null=True)
    field_world_weather_online_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_world_weather_online"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataFieldYahooWeather(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_yahoo_weather_format = CharField(index=True, null=True)
    field_yahoo_weather_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_field_yahoo_weather"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataNameField(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    name_field_format = CharField(index=True, null=True)
    name_field_value = CharField(null=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_data_name_field"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDataTitleField(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)
    title_field_format = CharField(index=True, null=True)
    title_field_value = CharField(null=True)

    class Meta:
        table_name = "moov_field_data_title_field"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDeletedData166(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_titre_de_l_annonce_format = CharField(index=True, null=True)
    field_titre_de_l_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_deleted_data_166"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDeletedData199(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_d_but_value = DateTimeField(null=True)
    field_date_d_but_value2 = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_deleted_data_199"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDeletedData200(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_datedeb_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_deleted_data_200"
        indexes = (
            (
                ("entity_type", "entity_id", "deleted", "delta", "language"),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted", "delta", "entity_id", "entity_type", "language"
        )


class FieldDeletedRevision166(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_titre_de_l_annonce_format = CharField(index=True, null=True)
    field_titre_de_l_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_deleted_revision_166"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldDeletedRevision199(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_d_but_value = DateTimeField(null=True)
    field_date_d_but_value2 = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_deleted_revision_199"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldDeletedRevision200(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_datedeb_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_deleted_revision_200"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldImageFieldCaption(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    caption = TextField(null=True)
    caption_format = CharField(null=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_name = CharField(constraints=[SQL("DEFAULT ''")])
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True, null=True)

    class Meta:
        table_name = "moov_field_image_field_caption"
        indexes = (
            (
                (
                    "field_name",
                    "entity_type",
                    "entity_id",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "delta", "entity_id", "entity_type", "field_name", "language"
        )


class FieldImageFieldCaptionRevision(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    caption = TextField(null=True)
    caption_format = CharField(null=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_name = CharField(constraints=[SQL("DEFAULT ''")])
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_image_field_caption_revision"
        indexes = (
            (
                (
                    "field_name",
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "delta",
            "entity_id",
            "entity_type",
            "field_name",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollBehavior(BaseModel):
    advpoll_behavior_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_behavior"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollChoice(BaseModel):
    advpoll_choice_choice = CharField()
    advpoll_choice_choice_id = CharField()
    advpoll_choice_write_in = IntegerField(constraints=[SQL("DEFAULT 0")])
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_choice"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollClosed(BaseModel):
    advpoll_closed_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_closed"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollCookieDuration(BaseModel):
    advpoll_cookie_duration_value = IntegerField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_cookie_duration"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollDates(BaseModel):
    advpoll_dates_value = DateTimeField(null=True)
    advpoll_dates_value2 = DateTimeField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_dates"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollMaxChoices(BaseModel):
    advpoll_max_choices_value = IntegerField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_max_choices"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollMode(BaseModel):
    advpoll_mode_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_mode"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollOptions(BaseModel):
    advpoll_options_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_options"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionAdvpollResults(BaseModel):
    advpoll_results_value = CharField(index=True, null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_advpoll_results"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionBody(BaseModel):
    body_format = CharField(index=True, null=True)
    body_summary = TextField(null=True)
    body_value = TextField(null=True)
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_body"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionCommentBody(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    comment_body_format = CharField(index=True, null=True)
    comment_body_value = TextField(null=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_comment_body"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionEventCalendarDate(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    event_calendar_date_value = DateTimeField(null=True)
    event_calendar_date_value2 = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_event_calendar_date"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionEventCalendarStatus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    event_calendar_status_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_event_calendar_status"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldAdressePharmacieGarde(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_adresse_pharmacie_garde_format = CharField(index=True, null=True)
    field_adresse_pharmacie_garde_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_adresse_pharmacie_garde"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldAfficherDansLaPageDAc(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_afficher_dans_la_page_d_ac_value = IntegerField(
        index=True, null=True
    )
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_afficher_dans_la_page_d_ac"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldAfficherDansLeSlider(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_afficher_dans_le_slider_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_afficher_dans_le_slider"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldArrivee(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_arrivee_format = CharField(index=True, null=True)
    field_arrivee_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_arrivee"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldArriveeDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_arrivee_du_vol_format = CharField(index=True, null=True)
    field_arrivee_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_arrivee_du_vol"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldAuteur(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_auteur_format = CharField(index=True, null=True)
    field_auteur_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_auteur"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldAutreTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_autre_t_l_phone_revision_id = IntegerField(index=True, null=True)
    field_autre_t_l_phone_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_autre_t_l_phone"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCatGorieDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_cat_gorie_de_l_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_cat_gorie_de_l_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCatGorieSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_cat_gorie_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_cat_gorie_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCategorieDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_de_l_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_categorie_de_l_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCategorieForum(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_forum_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_categorie_forum"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCategorieLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_live_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_categorie_live"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCategorieNumeroUrgence(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_categorie_numero_urgence_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_categorie_numero_urgence"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldChaNeTv(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_cha_ne_tv_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_cha_ne_tv"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldChannelId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_channel_id_format = CharField(index=True, null=True)
    field_channel_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_channel_id"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldChapeau(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_chapeau_format = CharField(index=True, null=True)
    field_chapeau_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_chapeau"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldChoisirCommeContact(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_choisir_comme_contact_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_choisir_comme_contact"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldChoixTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_choix_t_l_phone_revision_id = IntegerField(index=True, null=True)
    field_choix_t_l_phone_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_choix_t_l_phone"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldClouds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_clouds_format = CharField(index=True, null=True)
    field_clouds_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_clouds"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCodeProvince(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_code_province_format = CharField(index=True, null=True)
    field_code_province_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_code_province"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCodeRegion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_code_region_format = CharField(index=True, null=True)
    field_code_region_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_code_region"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCompagnieDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_compagnie_du_vol_format = CharField(index=True, null=True)
    field_compagnie_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_compagnie_du_vol"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCompteurAccueil(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_compteur_accueil_value = IntegerField(constraints=[SQL("DEFAULT 1")])
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_compteur_accueil"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCompteurCategorie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_compteur_categorie_value = CharField(
        constraints=[SQL("DEFAULT '1'")], null=True
    )
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_compteur_categorie"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldConditionDeVente(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_condition_de_vente_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_condition_de_vente"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldConditionDeVenteAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_condition_de_vente_annonce_format = CharField(index=True, null=True)
    field_condition_de_vente_annonce_summary = TextField(null=True)
    field_condition_de_vente_annonce_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_condition_de_vente_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldConditionDeVentePublici(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_condition_de_vente_publici_value = IntegerField(
        index=True, null=True
    )
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_condition_de_vente_publici"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldContact(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_contact"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldContactDesJournalistes(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_des_journalistes_format = CharField(index=True, null=True)
    field_contact_des_journalistes_summary = TextField(null=True)
    field_contact_des_journalistes_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_contact_des_journalistes"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldContactMe(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_me_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_contact_me"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldContactRapide(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_rapide__format = CharField(index=True, null=True)
    field_contact_rapide__value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_contact_rapide_"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldContactRapideAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contact_rapide_ads_format = CharField(index=True, null=True)
    field_contact_rapide_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_contact_rapide_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldContenuArticle(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_contenu_article_format = CharField(index=True, null=True)
    field_contenu_article_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_contenu_article"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightContenu(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_contenu"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightContenuDecouvri(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_decouvri_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_contenu_decouvri"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightContenuEducatio(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_educatio_format = CharField(index=True, null=True)
    field_copyright_contenu_educatio_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_contenu_educatio"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightContenuTendace(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_contenu_tendace_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_contenu_tendace"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightImageActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_actus_format = CharField(index=True, null=True)
    field_copyright_image_actus_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_image_actus"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightImageDecouvrir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_decouvrir_format = CharField(index=True, null=True)
    field_copyright_image_decouvrir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_image_decouvrir"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightImageEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_education_format = CharField(index=True, null=True)
    field_copyright_image_education_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_image_education"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightImageGallery(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_gallery_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_image_gallery"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCopyrightImageTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_copyright_image_tendance_format = CharField(index=True, null=True)
    field_copyright_image_tendance_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_copyright_image_tendance"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCourriel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_courriel_format = CharField(index=True, null=True)
    field_courriel_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_courriel"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCourse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_course_format = CharField(index=True, null=True)
    field_course_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_course"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldCouvertureOuiNon(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_couverture_oui_non_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_couverture_oui_non"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDPartDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_d_part_du_vol_format = CharField(index=True, null=True)
    field_d_part_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_d_part_du_vol"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDArrivE(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_d_arriv_e_format = CharField(index=True, null=True)
    field_date_d_arriv_e_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_d_arriv_e"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDeDButDiffusion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_d_but_diffusion_value = DateTimeField(null=True)
    field_date_de_d_but_diffusion_value2 = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_de_d_but_diffusion"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDeDiffusionAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_diffusion_ads_value = CharField(null=True)
    field_date_de_diffusion_ads_value2 = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_de_diffusion_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDeFinPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_fin_publicite_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_de_fin_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDePublication(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_de_publication_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_de_publication"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDebutDiffusion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_debut_diffusion_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_debut_diffusion"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDebutPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_debut_publicite_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_debut_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDuCours(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_cours_format = CharField(index=True, null=True)
    field_date_du_cours_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_du_cours"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDuCourse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_course_format = CharField(index=True, null=True)
    field_date_du_course_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_du_course"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDuProgramme(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_programme_format = CharField(index=True, null=True)
    field_date_du_programme_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_du_programme"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_du_vol_format = CharField(index=True, null=True)
    field_date_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_du_vol"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateEndAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_end_annonce_format = CharField(index=True, null=True)
    field_date_end_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_end_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateEndPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_end_publicite_format = CharField(index=True, null=True)
    field_date_end_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_end_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateEvenement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_evenement_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_evenement"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateFinDiffusion(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_fin_diffusion_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_fin_diffusion"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateMeteo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_meteo_format = CharField(index=True, null=True)
    field_date_meteo_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_meteo"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDatePartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_partenaire_value = DateTimeField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_partenaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDatePublicationAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_publication_annonce_format = CharField(index=True, null=True)
    field_date_publication_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_publication_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDatePublicationPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_publication_publicite_format = CharField(index=True, null=True)
    field_date_publication_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_publication_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_small_ads_value = CharField(null=True)
    field_date_small_ads_value2 = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateStartAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_start_annonce_format = CharField(index=True, null=True)
    field_date_start_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_start_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDateStartPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_date_start_publicite_format = CharField(index=True, null=True)
    field_date_start_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_date_start_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionActualite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_actualite_format = CharField(index=True, null=True)
    field_description_actualite_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_actualite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_de_l_annonce_format = CharField(index=True, null=True)
    field_description_de_l_annonce_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_de_l_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionDecouvrirMada(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_decouvrir_mada_format = CharField(index=True, null=True)
    field_description_decouvrir_mada_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_decouvrir_mada"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionECommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_e_commerce_format = CharField(index=True, null=True)
    field_description_e_commerce_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_e_commerce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_education_format = CharField(index=True, null=True)
    field_description_education_summary = TextField(null=True)
    field_description_education_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_education"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionEvenement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_evenement_format = CharField(index=True, null=True)
    field_description_evenement_summary = TextField(null=True)
    field_description_evenement_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_evenement"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionFilDinfo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_fil_dinfo_format = CharField(index=True, null=True)
    field_description_fil_dinfo_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_fil_dinfo"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionHotel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_hotel_format = CharField(index=True, null=True)
    field_description_hotel_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_hotel"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_partenaire_format = CharField(index=True, null=True)
    field_description_partenaire_summary = TextField(null=True)
    field_description_partenaire_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_partenaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_small_ads_format = CharField(index=True, null=True)
    field_description_small_ads_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_tendance_format = CharField(index=True, null=True)
    field_description_tendance_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_tendance"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDescriptionUtilisateur(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_description_utilisateur_format = CharField(index=True, null=True)
    field_description_utilisateur_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_description_utilisateur"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDestination(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_destination_format = CharField(index=True, null=True)
    field_destination_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_destination"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldDevise(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_devise_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_devise"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldEMailProfessionnel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_e_mail_professionnel_format = CharField(index=True, null=True)
    field_e_mail_professionnel_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_e_mail_professionnel"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldEmailProfessionnelAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_email_professionnel_ads_format = CharField(index=True, null=True)
    field_email_professionnel_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_email_professionnel_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldEmplacement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_emplacement"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldEmplacementDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_de_l_annonce_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_emplacement_de_l_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldEmplacementDisponiblePub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_disponible_pub_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_emplacement_disponible_pub"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldEmplacementDuPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_emplacement_du_pub_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_emplacement_du_pub_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldFeedItemDescription(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_feed_item_description_format = CharField(index=True, null=True)
    field_feed_item_description_summary = TextField(null=True)
    field_feed_item_description_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_feed_item_description"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldFluxRssConnectedLife(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_connected_life_format = CharField(index=True, null=True)
    field_flux_rss_connected_life_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_flux_rss_connected_life"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldFluxRssInternationale(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_internationale_format = CharField(index=True, null=True)
    field_flux_rss_internationale_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_flux_rss_internationale"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldFluxRssMedecineEtSante(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_medecine_et_sante_format = CharField(index=True, null=True)
    field_flux_rss_medecine_et_sante_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_flux_rss_medecine_et_sante"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldFluxRssPeople(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_flux_rss_people_format = CharField(index=True, null=True)
    field_flux_rss_people_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_flux_rss_people"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldFormatDuPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_format_du_pub_format = CharField(index=True, null=True)
    field_format_du_pub_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_format_du_pub"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldFormatDuPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_format_du_pub_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_format_du_pub_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldGrilleTarifaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_grille_tarifaire_format = CharField(null=True)
    field_grille_tarifaire_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_grille_tarifaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldGrilleTarifairePublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_grille_tarifaire_publicite_format = CharField(null=True)
    field_grille_tarifaire_publicite_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_grille_tarifaire_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldGuideAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_guide_annonce_format = CharField(index=True, null=True)
    field_guide_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_guide_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldHeureArrivE(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_arriv_e_format = CharField(index=True, null=True)
    field_heure_arriv_e_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_heure_arriv_e"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldHeureDPart(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_d_part_format = CharField(index=True, null=True)
    field_heure_d_part_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_heure_d_part"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldHeureDuProgramme(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_du_programme_format = CharField(index=True, null=True)
    field_heure_du_programme_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_heure_du_programme"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldHeureSortir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_heure_sortir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_heure_sortir"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldHomepage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_homepage_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_homepage"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldHumidite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_humidite_format = CharField(index=True, null=True)
    field_humidite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_humidite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldIcone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_alt = CharField(null=True)
    field_icone_fid = IntegerField(index=True, null=True)
    field_icone_height = IntegerField(null=True)
    field_icone_title = CharField(null=True)
    field_icone_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_icone"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldIconeActualites(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_actualites_format = CharField(index=True, null=True)
    field_icone_actualites_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_icone_actualites"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldIconeDCouvrirMCar(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_d_couvrir_m_car_format = CharField(index=True, null=True)
    field_icone_d_couvrir_m_car_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_icone_d_couvrir_m_car"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldIconeTendanceMoov(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_icone_tendance_moov_format = CharField(index=True, null=True)
    field_icone_tendance_moov_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_icone_tendance_moov"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_id_format = CharField(index=True, null=True)
    field_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_id"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_alt = CharField(null=True)
    field_image_fid = IntegerField(index=True, null=True)
    field_image_height = IntegerField(null=True)
    field_image_title = CharField(null=True)
    field_image_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_actus_alt = CharField(null=True)
    field_image_actus_fid = IntegerField(index=True, null=True)
    field_image_actus_height = IntegerField(null=True)
    field_image_actus_title = CharField(null=True)
    field_image_actus_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_actus"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageAnnonceDefault(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_annonce_default_alt = CharField(null=True)
    field_image_annonce_default_fid = IntegerField(index=True, null=True)
    field_image_annonce_default_height = IntegerField(null=True)
    field_image_annonce_default_title = CharField(null=True)
    field_image_annonce_default_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_annonce_default"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageDeCouvertureLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_couverture_live_alt = CharField(null=True)
    field_image_de_couverture_live_fid = IntegerField(index=True, null=True)
    field_image_de_couverture_live_height = IntegerField(null=True)
    field_image_de_couverture_live_title = CharField(null=True)
    field_image_de_couverture_live_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_de_couverture_live"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageDeLAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_l_annonce_alt = CharField(null=True)
    field_image_de_l_annonce_fid = IntegerField(index=True, null=True)
    field_image_de_l_annonce_height = IntegerField(null=True)
    field_image_de_l_annonce_title = CharField(null=True)
    field_image_de_l_annonce_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_de_l_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageDeLaPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_la_pub_alt = CharField(null=True)
    field_image_de_la_pub_fid = IntegerField(index=True, null=True)
    field_image_de_la_pub_height = IntegerField(null=True)
    field_image_de_la_pub_title = CharField(null=True)
    field_image_de_la_pub_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_de_la_pub"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageDeLaPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_de_la_pub_ads_alt = CharField(null=True)
    field_image_de_la_pub_ads_fid = IntegerField(index=True, null=True)
    field_image_de_la_pub_ads_height = IntegerField(null=True)
    field_image_de_la_pub_ads_title = CharField(null=True)
    field_image_de_la_pub_ads_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_de_la_pub_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageECommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_e_commerce_alt = CharField(null=True)
    field_image_e_commerce_fid = IntegerField(index=True, null=True)
    field_image_e_commerce_height = IntegerField(null=True)
    field_image_e_commerce_title = CharField(null=True)
    field_image_e_commerce_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_e_commerce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_education_alt = CharField(null=True)
    field_image_education_fid = IntegerField(index=True, null=True)
    field_image_education_height = IntegerField(null=True)
    field_image_education_title = CharField(null=True)
    field_image_education_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_education"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageEvent(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_event_alt = CharField(null=True)
    field_image_event_fid = IntegerField(index=True, null=True)
    field_image_event_height = IntegerField(null=True)
    field_image_event_title = CharField(null=True)
    field_image_event_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_event"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageGuide(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_guide_alt = CharField(null=True)
    field_image_guide_fid = IntegerField(index=True, null=True)
    field_image_guide_height = IntegerField(null=True)
    field_image_guide_title = CharField(null=True)
    field_image_guide_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_guide"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageLogo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_logo_alt = CharField(null=True)
    field_image_logo_fid = IntegerField(index=True, null=True)
    field_image_logo_height = IntegerField(null=True)
    field_image_logo_title = CharField(null=True)
    field_image_logo_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_logo"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageParDefautAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_par_defaut_annonce_alt = CharField(null=True)
    field_image_par_defaut_annonce_fid = IntegerField(index=True, null=True)
    field_image_par_defaut_annonce_height = IntegerField(null=True)
    field_image_par_defaut_annonce_title = CharField(null=True)
    field_image_par_defaut_annonce_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_par_defaut_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagePopin(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_popin_alt = CharField(null=True)
    field_image_popin_fid = IntegerField(index=True, null=True)
    field_image_popin_height = IntegerField(null=True)
    field_image_popin_title = CharField(null=True)
    field_image_popin_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_popin"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagePubFooter(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_pub_footer_alt = CharField(null=True)
    field_image_pub_footer_class = CharField(null=True)
    field_image_pub_footer_fid = IntegerField(index=True, null=True)
    field_image_pub_footer_height = IntegerField(null=True)
    field_image_pub_footer_longdesc = CharField(null=True)
    field_image_pub_footer_rel = CharField(null=True)
    field_image_pub_footer_target = CharField(null=True)
    field_image_pub_footer_title = CharField(null=True)
    field_image_pub_footer_url = CharField(null=True)
    field_image_pub_footer_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_pub_footer"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagePubHautPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_pub_haut_pub_alt = CharField(null=True)
    field_image_pub_haut_pub_class = CharField(null=True)
    field_image_pub_haut_pub_fid = IntegerField(index=True, null=True)
    field_image_pub_haut_pub_height = IntegerField(null=True)
    field_image_pub_haut_pub_longdesc = CharField(null=True)
    field_image_pub_haut_pub_rel = CharField(null=True)
    field_image_pub_haut_pub_target = CharField(null=True)
    field_image_pub_haut_pub_title = CharField(null=True)
    field_image_pub_haut_pub_url = CharField(null=True)
    field_image_pub_haut_pub_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_pub_haut_pub"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_small_ads_alt = CharField(null=True)
    field_image_small_ads_fid = IntegerField(index=True, null=True)
    field_image_small_ads_height = IntegerField(null=True)
    field_image_small_ads_title = CharField(null=True)
    field_image_small_ads_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageVolutionDuDevise(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_volution_du_devise_alt = CharField(null=True)
    field_image_volution_du_devise_fid = IntegerField(index=True, null=True)
    field_image_volution_du_devise_height = IntegerField(null=True)
    field_image_volution_du_devise_title = CharField(null=True)
    field_image_volution_du_devise_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_volution_du_devise"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageVotrePubSurMoov(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_image_votre_pub_sur_moov_alt = CharField(null=True)
    field_image_votre_pub_sur_moov_fid = IntegerField(index=True, null=True)
    field_image_votre_pub_sur_moov_height = IntegerField(null=True)
    field_image_votre_pub_sur_moov_title = CharField(null=True)
    field_image_votre_pub_sur_moov_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_image_votre_pub_sur_moov"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImages(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_revision_id = IntegerField(index=True, null=True)
    field_images_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_images"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagesActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_actus_revision_id = IntegerField(index=True, null=True)
    field_images_actus_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_images_actus"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagesFondPublicitaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_fond_publicitaire_alt = CharField(null=True)
    field_images_fond_publicitaire_fid = IntegerField(index=True, null=True)
    field_images_fond_publicitaire_height = IntegerField(null=True)
    field_images_fond_publicitaire_title = CharField(null=True)
    field_images_fond_publicitaire_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_images_fond_publicitaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagesLookDuJour(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_look_du_jour_alt = CharField(null=True)
    field_images_look_du_jour_fid = IntegerField(index=True, null=True)
    field_images_look_du_jour_height = IntegerField(null=True)
    field_images_look_du_jour_title = CharField(null=True)
    field_images_look_du_jour_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_images_look_du_jour"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagesPubBas(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_pub_bas_alt = CharField(null=True)
    field_images_pub_bas_class = CharField(null=True)
    field_images_pub_bas_fid = IntegerField(index=True, null=True)
    field_images_pub_bas_height = IntegerField(null=True)
    field_images_pub_bas_longdesc = CharField(null=True)
    field_images_pub_bas_rel = CharField(null=True)
    field_images_pub_bas_target = CharField(null=True)
    field_images_pub_bas_title = CharField(null=True)
    field_images_pub_bas_url = CharField(null=True)
    field_images_pub_bas_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_images_pub_bas"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagesPubCarrebas(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_pub_carrebas_alt = CharField(null=True)
    field_images_pub_carrebas_class = CharField(null=True)
    field_images_pub_carrebas_fid = IntegerField(index=True, null=True)
    field_images_pub_carrebas_height = IntegerField(null=True)
    field_images_pub_carrebas_longdesc = CharField(null=True)
    field_images_pub_carrebas_rel = CharField(null=True)
    field_images_pub_carrebas_target = CharField(null=True)
    field_images_pub_carrebas_title = CharField(null=True)
    field_images_pub_carrebas_url = CharField(null=True)
    field_images_pub_carrebas_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_images_pub_carrebas"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImagesPubCarrehaut(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_images_pub_carrehaut_alt = CharField(null=True)
    field_images_pub_carrehaut_class = CharField(null=True)
    field_images_pub_carrehaut_fid = IntegerField(index=True, null=True)
    field_images_pub_carrehaut_height = IntegerField(null=True)
    field_images_pub_carrehaut_longdesc = CharField(null=True)
    field_images_pub_carrehaut_rel = CharField(null=True)
    field_images_pub_carrehaut_target = CharField(null=True)
    field_images_pub_carrehaut_title = CharField(null=True)
    field_images_pub_carrehaut_url = CharField(null=True)
    field_images_pub_carrehaut_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_images_pub_carrehaut"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldImageschamps(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_imageschamps_alt = CharField(null=True)
    field_imageschamps_fid = IntegerField(index=True, null=True)
    field_imageschamps_height = IntegerField(null=True)
    field_imageschamps_title = CharField(null=True)
    field_imageschamps_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_imageschamps"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLibelle(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_libelle_format = CharField(index=True, null=True)
    field_libelle_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_libelle"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienDuPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_du_partenaire_format = CharField(index=True, null=True)
    field_lien_du_partenaire_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_du_partenaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienHotel(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_hotel_format = CharField(index=True, null=True)
    field_lien_hotel_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_hotel"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienImage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_image_format = CharField(index=True, null=True)
    field_lien_image_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_image"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienImagePublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_image_publicite_format = CharField(index=True, null=True)
    field_lien_image_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_image_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_live_format = CharField(index=True, null=True)
    field_lien_live_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_live"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienSortir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sortir_format = CharField(index=True, null=True)
    field_lien_sortir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_sortir"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienSponsorisActus(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_actus_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_sponsoris_actus"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienSponsorisDecouvrir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_decouvrir_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_sponsoris_decouvrir"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienSponsorisEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_education_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_sponsoris_education"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienSponsorisTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_sponsoris_tendance_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_sponsoris_tendance"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLienVotrePubSurMoov(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lien_votre_pub_sur_moov_format = CharField(index=True, null=True)
    field_lien_votre_pub_sur_moov_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lien_votre_pub_sur_moov"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLieuAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lieu_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLieuEntityform(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_entityform_format = CharField(index=True, null=True)
    field_lieu_entityform_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lieu_entityform"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLieuEvenement(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_evenement_format = CharField(index=True, null=True)
    field_lieu_evenement_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lieu_evenement"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLieuPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_partenaire_format = CharField(index=True, null=True)
    field_lieu_partenaire_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lieu_partenaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLieuSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_lieu_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_lieu_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldListesDesProvinces(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_listes_des_provinces_format = CharField(index=True, null=True)
    field_listes_des_provinces_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_listes_des_provinces"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLogoCopyright(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_alt = CharField(null=True)
    field_logo_copyright_fid = IntegerField(index=True, null=True)
    field_logo_copyright_height = IntegerField(null=True)
    field_logo_copyright_title = CharField(null=True)
    field_logo_copyright_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_logo_copyright"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLogoCopyrightDecouvrir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_decouvrir_alt = CharField(null=True)
    field_logo_copyright_decouvrir_fid = IntegerField(index=True, null=True)
    field_logo_copyright_decouvrir_height = IntegerField(null=True)
    field_logo_copyright_decouvrir_title = CharField(null=True)
    field_logo_copyright_decouvrir_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_logo_copyright_decouvrir"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLogoCopyrightEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_education_alt = CharField(null=True)
    field_logo_copyright_education_fid = IntegerField(index=True, null=True)
    field_logo_copyright_education_height = IntegerField(null=True)
    field_logo_copyright_education_title = CharField(null=True)
    field_logo_copyright_education_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_logo_copyright_education"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLogoCopyrightTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_copyright_tendance_alt = CharField(null=True)
    field_logo_copyright_tendance_fid = IntegerField(index=True, null=True)
    field_logo_copyright_tendance_height = IntegerField(null=True)
    field_logo_copyright_tendance_title = CharField(null=True)
    field_logo_copyright_tendance_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_logo_copyright_tendance"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLogoLive(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_live_alt = CharField(null=True)
    field_logo_live_fid = IntegerField(index=True, null=True)
    field_logo_live_height = IntegerField(null=True)
    field_logo_live_title = CharField(null=True)
    field_logo_live_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_logo_live"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLogoMedia(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_media_alt = CharField(null=True)
    field_logo_media_fid = IntegerField(index=True, null=True)
    field_logo_media_height = IntegerField(null=True)
    field_logo_media_title = CharField(null=True)
    field_logo_media_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_logo_media"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldLogoPartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_logo_partenaire_alt = CharField(null=True)
    field_logo_partenaire_fid = IntegerField(index=True, null=True)
    field_logo_partenaire_height = IntegerField(null=True)
    field_logo_partenaire_title = CharField(null=True)
    field_logo_partenaire_width = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_logo_partenaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMeteo(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_meteo_format = CharField(index=True, null=True)
    field_meteo_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_meteo"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMeteoweek(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_meteoweek_format = CharField(index=True, null=True)
    field_meteoweek_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_meteoweek"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMettreEnCouverture(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_mettre_en_couverture_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_mettre_en_couverture"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldModRationCondition(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_mod_ration_condition_format = CharField(index=True, null=True)
    field_mod_ration_condition_summary = TextField(null=True)
    field_mod_ration_condition_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_mod_ration_condition"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMontantDeLaPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_de_la_publicite_format = CharField(index=True, null=True)
    field_montant_de_la_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_montant_de_la_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMontantEnAriary(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_en_ariary_format = CharField(index=True, null=True)
    field_montant_en_ariary_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_montant_en_ariary"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMontantPayer(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_payer_format = CharField(index=True, null=True)
    field_montant_payer_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_montant_payer"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMontantPayerSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_payer_small_ads_format = CharField(index=True, null=True)
    field_montant_payer_small_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_montant_payer_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMontantPubliciteAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_montant_publicite_ads_format = CharField(index=True, null=True)
    field_montant_publicite_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_montant_publicite_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldMvolaPharmacie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_mvola_pharmacie_format = CharField(index=True, null=True)
    field_mvola_pharmacie_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_mvola_pharmacie"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNom(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_format = CharField(index=True, null=True)
    field_nom_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nom"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNomDeLaSociete(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_de_la_societe_format = CharField(index=True, null=True)
    field_nom_de_la_societe_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nom_de_la_societe"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNomDuPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_du_pub_format = CharField(index=True, null=True)
    field_nom_du_pub_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nom_du_pub"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNomSocieteAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nom_societe_ads_format = CharField(index=True, null=True)
    field_nom_societe_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nom_societe_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNombreDeJourAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_ads_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nombre_de_jour_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNombreDeJourAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_annonce_format = CharField(index=True, null=True)
    field_nombre_de_jour_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nombre_de_jour_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNombreDeJourPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_publicite_value = IntegerField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nombre_de_jour_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNombreDeJourSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_jour_small_ads_format = CharField(index=True, null=True)
    field_nombre_de_jour_small_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nombre_de_jour_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNombreDeTransaction(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nombre_de_transaction_format = CharField(index=True, null=True)
    field_nombre_de_transaction_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nombre_de_transaction"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNomicone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_nomicone_format = CharField(index=True, null=True)
    field_nomicone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_nomicone"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNumero(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_format = CharField(index=True, null=True)
    field_numero_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_numero"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNumeroDeLaPubAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_de_la_pub_ads_format = CharField(index=True, null=True)
    field_numero_de_la_pub_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_numero_de_la_pub_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNumeroDeTelephone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_de_telephone_format = CharField(index=True, null=True)
    field_numero_de_telephone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_numero_de_telephone"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNumeroDeTelephoneAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_de_telephone_ads_format = CharField(index=True, null=True)
    field_numero_de_telephone_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_numero_de_telephone_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNumeroTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_t_l_phone_format = CharField(index=True, null=True)
    field_numero_t_l_phone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_numero_t_l_phone"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldNumeroTphAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_numero_tph_annonce_format = CharField(index=True, null=True)
    field_numero_tph_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_numero_tph_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldOrigine(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_origine_format = CharField(index=True, null=True)
    field_origine_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_origine"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPageDeLaPubliciteAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_page_de_la_publicite_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_page_de_la_publicite_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPetitesAnnoncesId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_petites_annonces_id_format = CharField(index=True, null=True)
    field_petites_annonces_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_petites_annonces_id"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPhoneNumber(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_phone_number_format = CharField(index=True, null=True)
    field_phone_number_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_phone_number"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPrNoms(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_pr_noms_format = CharField(index=True, null=True)
    field_pr_noms_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_pr_noms"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPressure(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_pressure_format = CharField(index=True, null=True)
    field_pressure_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_pressure"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPrice(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_price_format = CharField(index=True, null=True)
    field_price_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_price"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPrixEnAriary(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_prix_en_ariary_value = FloatField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_prix_en_ariary"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldPubliciteId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_publicite_id_format = CharField(index=True, null=True)
    field_publicite_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_publicite_id"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuartBnous4Rapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_bnous_4_rapport_format = CharField(index=True, null=True)
    field_quart_bnous_4_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quart_bnous_4_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuartBonus4Isa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_bonus_4_isa_format = CharField(index=True, null=True)
    field_quart_bonus_4_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quart_bonus_4_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuartDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_desordre_isa_format = CharField(index=True, null=True)
    field_quart_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quart_desordre_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuartDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_desordre_rapport_format = CharField(index=True, null=True)
    field_quart_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quart_desordre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuartOrdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quart_ordre_rapport_format = CharField(index=True, null=True)
    field_quart_ordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quart_ordre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuarteOrdreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quarte_ordre_isa_format = CharField(index=True, null=True)
    field_quarte_ordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quarte_ordre_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuintBonusIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_bonus_isa_format = CharField(index=True, null=True)
    field_quint_bonus_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quint_bonus_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuintBonusRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_bonus_rapport_format = CharField(index=True, null=True)
    field_quint_bonus_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quint_bonus_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuintDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_desordre_isa_format = CharField(index=True, null=True)
    field_quint_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quint_desordre_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuintDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_desordre_rapport_format = CharField(index=True, null=True)
    field_quint_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quint_desordre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuintOrdreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_ordre_isa_format = CharField(index=True, null=True)
    field_quint_ordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quint_ordre_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldQuintOrdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_quint_ordre_rapport_format = CharField(index=True, null=True)
    field_quint_ordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_quint_ordre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldRFRenceDePaiementMvol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_r_f_rence_de_paiement_mvol_format = CharField(index=True, null=True)
    field_r_f_rence_de_paiement_mvol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_r_f_rence_de_paiement_mvol"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldRFRencePaiementMvola(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_r_f_rence_paiement_mvola_format = CharField(index=True, null=True)
    field_r_f_rence_paiement_mvola_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_r_f_rence_paiement_mvola"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldRGionPharmacieListe(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_r_gion_pharmacie_liste_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_r_gion_pharmacie_liste"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldReferenceMvola(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_reference_mvola_format = CharField(index=True, null=True)
    field_reference_mvola_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_reference_mvola"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldReferenceMvolaAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_reference_mvola_ads_format = CharField(index=True, null=True)
    field_reference_mvola_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_reference_mvola_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldReponse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_reponse_format = CharField(index=True, null=True)
    field_reponse_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_reponse"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldRestricitonMineurForum(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_restriciton_mineur_forum_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_restriciton_mineur_forum"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldRestrictionMineurCondit(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_restriction_mineur_condit_format = CharField(index=True, null=True)
    field_restriction_mineur_condit_summary = TextField(null=True)
    field_restriction_mineur_condit_value = TextField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_restriction_mineur_condit"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldRubriqueCategorie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_rubrique_categorie_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_rubrique_categorie"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSaisirNouveauNumero(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_saisir_nouveau_numero_format = CharField(index=True, null=True)
    field_saisir_nouveau_numero_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_saisir_nouveau_numero"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSaisirUnNouveauEmail(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_saisir_un_nouveau_email_email = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_saisir_un_nouveau_email"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSemaineDeGarde(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_semaine_de_garde_format = CharField(index=True, null=True)
    field_semaine_de_garde_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_semaine_de_garde"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSixteBonus4Isa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_bonus_4_isa_format = CharField(index=True, null=True)
    field_sixte_bonus_4_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sixte_bonus_4_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSixteBonus4Rapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_bonus_4_rapport_format = CharField(index=True, null=True)
    field_sixte_bonus_4_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sixte_bonus_4_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSixteDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_desordre_isa_format = CharField(index=True, null=True)
    field_sixte_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sixte_desordre_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSixteDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_desordre_rapport_format = CharField(index=True, null=True)
    field_sixte_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sixte_desordre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSixteOdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_odre_rapport_format = CharField(index=True, null=True)
    field_sixte_odre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sixte_odre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSixteOrdre(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sixte_ordre_format = CharField(index=True, null=True)
    field_sixte_ordre_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sixte_ordre"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSliderPageAccueil(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_slider_page_accueil_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_slider_page_accueil"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSliderPageCategorie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_slider_page_categorie_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_slider_page_categorie"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSliderPageCategorieIn(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_slider_page_categorie_in_value = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_slider_page_categorie_in"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSourceCours(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_source_cours_format = CharField(index=True, null=True)
    field_source_cours_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_source_cours"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSousCatGorieAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_cat_gorie_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sous_cat_gorie_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSousCategorieSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_categorie_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sous_categorie_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSousTitreEducation(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_titre_education_format = CharField(index=True, null=True)
    field_sous_titre_education_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sous_titre_education"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldSousTitreTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_sous_titre_tendance_format = CharField(index=True, null=True)
    field_sous_titre_tendance_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_sous_titre_tendance"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldStatusDeLaTransaction(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_status_de_la_transaction_format = CharField(index=True, null=True)
    field_status_de_la_transaction_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_status_de_la_transaction"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldStatusTransactionPub(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_status_transaction_pub_format = CharField(index=True, null=True)
    field_status_transaction_pub_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_status_transaction_pub"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldStatutTransactionAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_statut_transaction_ads_format = CharField(index=True, null=True)
    field_statut_transaction_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_statut_transaction_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTLPhone(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_t_l_phone_format = CharField(index=True, null=True)
    field_t_l_phone_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_t_l_phone"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTags(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tags_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_tags"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTelephonePharmacie(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_telephone_pharmacie_format = CharField(index=True, null=True)
    field_telephone_pharmacie_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_telephone_pharmacie"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTemperatureJour(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_jour_format = CharField(index=True, null=True)
    field_temperature_jour_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_temperature_jour"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTemperatureMatin(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_matin_format = CharField(index=True, null=True)
    field_temperature_matin_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_temperature_matin"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTemperatureMax(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_max_format = CharField(index=True, null=True)
    field_temperature_max_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_temperature_max"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTemperatureNuit(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_nuit_format = CharField(index=True, null=True)
    field_temperature_nuit_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_temperature_nuit"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTemperatureSoir(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_temperature_soir_format = CharField(index=True, null=True)
    field_temperature_soir_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_temperature_soir"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTierceBonusIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_bonus_isa_format = CharField(index=True, null=True)
    field_tierce_bonus_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_tierce_bonus_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTierceDesordreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_desordre_isa_format = CharField(index=True, null=True)
    field_tierce_desordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_tierce_desordre_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTierceDesordreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_desordre_rapport_format = CharField(index=True, null=True)
    field_tierce_desordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_tierce_desordre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTierceOrdreIsa(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_ordre_isa_format = CharField(index=True, null=True)
    field_tierce_ordre_isa_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_tierce_ordre_isa"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTierceOrdreRapport(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_tierce_ordre_rapport_format = CharField(index=True, null=True)
    field_tierce_ordre_rapport_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_tierce_ordre_rapport"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTitreAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_titre_annonce_format = CharField(index=True, null=True)
    field_titre_annonce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_titre_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTitreTest(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_titre_test_format = CharField(index=True, null=True)
    field_titre_test_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_titre_test"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTokenId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_token_id_format = CharField(index=True, null=True)
    field_token_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_token_id"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTokenIdAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_token_id_ads_format = CharField(index=True, null=True)
    field_token_id_ads_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_token_id_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTokenIdPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_token_id_publicite_format = CharField(index=True, null=True)
    field_token_id_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_token_id_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTransactionId(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_transaction_id_format = CharField(index=True, null=True)
    field_transaction_id_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_transaction_id"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTransactionIdPublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_transaction_id_publicite_format = CharField(index=True, null=True)
    field_transaction_id_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_transaction_id_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeActualite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_actualite_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_actualite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeDeCondition(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_condition_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_de_condition"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeDeMedia(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_media_value = CharField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_de_media"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeDeVidO(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_vid_o_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_de_vid_o"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeDeVotreAnnonce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_de_votre_annonce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_de_votre_annonce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeDecouvrirMadagascar(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_decouvrir_madagascar_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_decouvrir_madagascar"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeDuProgramme(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_du_programme_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_du_programme"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeDuVol(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_du_vol_format = CharField(index=True, null=True)
    field_type_du_vol_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_du_vol"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeECommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_e_commerce_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_e_commerce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeSmallAds(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_small_ads_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_small_ads"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldTypeTendance(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_type_tendance_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_type_tendance"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlMedia(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_media_format = CharField(index=True, null=True)
    field_url_media_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_media"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPageEcommerce(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_ecommerce_format = CharField(index=True, null=True)
    field_url_page_ecommerce_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_ecommerce"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPageEmploi(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_emploi_format = CharField(index=True, null=True)
    field_url_page_emploi_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_emploi"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPageIframe(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_iframe_format = CharField(index=True, null=True)
    field_url_page_iframe_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_iframe"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPagePmu(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_pmu_format = CharField(index=True, null=True)
    field_url_page_pmu_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_pmu"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPagePratiqueReservez(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_pratique_reservez_format = CharField(index=True, null=True)
    field_url_page_pratique_reservez_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_pratique_reservez"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPageRelooking(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_relooking_format = CharField(index=True, null=True)
    field_url_page_relooking_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_relooking"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPageSelfcare(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_selfcare_format = CharField(index=True, null=True)
    field_url_page_selfcare_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_selfcare"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlPageVotrePublicite(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_page_votre_publicite_format = CharField(index=True, null=True)
    field_url_page_votre_publicite_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_page_votre_publicite"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldUrlVidO(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_url_vid_o_format = CharField(index=True, null=True)
    field_url_vid_o_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_url_vid_o"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVidOEvent(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_vid_o_event_format = CharField(index=True, null=True)
    field_vid_o_event_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_vid_o_event"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVidOStreaming(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_vid_o_streaming_description = TextField(null=True)
    field_vid_o_streaming_display = IntegerField(
        constraints=[SQL("DEFAULT 1")]
    )
    field_vid_o_streaming_fid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_vid_o_streaming"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVideoUrl(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_video_url_format = CharField(index=True, null=True)
    field_video_url_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_video_url"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVideosDuJour(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_videos_du_jour_format = CharField(index=True, null=True)
    field_videos_du_jour_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_videos_du_jour"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVille(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_ville_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_ville"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVillePartenaire(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_ville_partenaire_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_ville_partenaire"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVitesse(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_vitesse_format = CharField(index=True, null=True)
    field_vitesse_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_vitesse"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVolume(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_volume_format = CharField(index=True, null=True)
    field_volume_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_volume"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldVotrePubDansLaPage(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_votre_pub_dans_la_page_tid = IntegerField(index=True, null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_votre_pub_dans_la_page"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldWeatherCom(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_weather_com_format = CharField(index=True, null=True)
    field_weather_com_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_weather_com"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldWorldWeatherOnline(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_world_weather_online_format = CharField(index=True, null=True)
    field_world_weather_online_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_world_weather_online"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionFieldYahooWeather(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    field_yahoo_weather_format = CharField(index=True, null=True)
    field_yahoo_weather_value = CharField(null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_field_yahoo_weather"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionNameField(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    name_field_format = CharField(index=True, null=True)
    name_field_value = CharField(null=True)
    revision_id = IntegerField(index=True)

    class Meta:
        table_name = "moov_field_revision_name_field"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldRevisionTitleField(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delta = IntegerField()
    entity_id = IntegerField(index=True)
    entity_type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    revision_id = IntegerField(index=True)
    title_field_format = CharField(index=True, null=True)
    title_field_value = CharField(null=True)

    class Meta:
        table_name = "moov_field_revision_title_field"
        indexes = (
            (
                (
                    "entity_type",
                    "entity_id",
                    "revision_id",
                    "deleted",
                    "delta",
                    "language",
                ),
                True,
            ),
        )
        primary_key = CompositeKey(
            "deleted",
            "delta",
            "entity_id",
            "entity_type",
            "language",
            "revision_id",
        )


class FieldValidationRule(BaseModel):
    bundle = CharField(constraints=[SQL("DEFAULT ''")])
    col = CharField(constraints=[SQL("DEFAULT 'value'")])
    entity_type = CharField(constraints=[SQL("DEFAULT ''")])
    error_message = CharField(null=True)
    field_name = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    ruleid = AutoField()
    rulename = CharField(constraints=[SQL("DEFAULT ''")])
    settings = TextField(null=True)
    validator = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_field_validation_rule"
        indexes = ((("field_name", "entity_type", "bundle"), False),)


class FileManaged(BaseModel):
    fid = AutoField()
    filemime = CharField(constraints=[SQL("DEFAULT ''")])
    filename = CharField(constraints=[SQL("DEFAULT ''")])
    filesize = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    uri = CharField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = "moov_file_managed"


class FileUsage(BaseModel):
    count = IntegerField(constraints=[SQL("DEFAULT 0")])
    fid = IntegerField()
    id = IntegerField(constraints=[SQL("DEFAULT 0")])
    module = CharField(constraints=[SQL("DEFAULT ''")])
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_file_usage"
        indexes = (
            (("fid", "count"), False),
            (("fid", "module"), False),
            (("fid", "type", "id", "module"), True),
            (("type", "id"), False),
        )
        primary_key = CompositeKey("fid", "id", "module", "type")


class Filter(BaseModel):
    format = CharField()
    module = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    settings = TextField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_filter"
        indexes = (
            (("format", "name"), True),
            (("weight", "module", "name"), False),
        )
        primary_key = CompositeKey("format", "name")


class FilterFormat(BaseModel):
    cache = IntegerField(constraints=[SQL("DEFAULT 0")])
    format = CharField(primary_key=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_filter_format"
        indexes = ((("status", "weight"), False),)


class Flag(BaseModel):
    entity_type = CharField(constraints=[SQL("DEFAULT ''")])
    fid = AutoField()
    global_ = IntegerField(
        column_name="global", constraints=[SQL("DEFAULT 0")], null=True
    )
    name = CharField(constraints=[SQL("DEFAULT ''")], null=True, unique=True)
    options = TextField(null=True)
    title = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = "moov_flag"


class FlagActions(BaseModel):
    aid = AutoField()
    callback = CharField(constraints=[SQL("DEFAULT ''")])
    event = CharField(null=True)
    fid = IntegerField(null=True)
    parameters = TextField()
    repeat_threshold = IntegerField(constraints=[SQL("DEFAULT 0")])
    threshold = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_flag_actions"


class FlagCounts(BaseModel):
    count = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_type = CharField(constraints=[SQL("DEFAULT ''")])
    fid = IntegerField(constraints=[SQL("DEFAULT 0")])
    last_updated = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_flag_counts"
        indexes = (
            (("entity_type", "entity_id"), False),
            (("fid", "count"), False),
            (("fid", "entity_id"), True),
            (("fid", "entity_type"), False),
            (("fid", "last_updated"), False),
        )
        primary_key = CompositeKey("entity_id", "fid")


class FlagTypes(BaseModel):
    fid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_flag_types"
        primary_key = False


class Flagging(BaseModel):
    entity_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_type = CharField(constraints=[SQL("DEFAULT ''")])
    fid = IntegerField(constraints=[SQL("DEFAULT 0")])
    flagging_id = AutoField()
    sid = IntegerField(constraints=[SQL("DEFAULT 0")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_flagging"
        indexes = (
            (("entity_id", "fid"), False),
            (("entity_type", "entity_id", "uid", "sid"), False),
            (("entity_type", "uid", "sid"), False),
            (("fid", "entity_id", "uid", "sid"), True),
        )


class FlexsliderOptionset(BaseModel):
    name = CharField(primary_key=True)
    options = TextField(null=True)
    theme = CharField(constraints=[SQL("DEFAULT 'classic'")])
    title = CharField()

    class Meta:
        table_name = "moov_flexslider_optionset"


class Flood(BaseModel):
    event = CharField(constraints=[SQL("DEFAULT ''")])
    expiration = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    fid = AutoField()
    identifier = CharField(constraints=[SQL("DEFAULT ''")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_flood"
        indexes = ((("event", "identifier", "timestamp"), False),)


class FormBuilderCache(BaseModel):
    data = TextField(null=True)
    form_id = CharField(null=True)
    sid = CharField(null=True)
    type = CharField(null=True)
    updated = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_form_builder_cache"
        indexes = ((("sid", "type", "form_id"), False),)
        primary_key = False


class Forum(BaseModel):
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    tid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    vid = AutoField()

    class Meta:
        table_name = "moov_forum"
        indexes = ((("nid", "tid"), False),)


class ForumIndex(BaseModel):
    comment_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    created = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    last_comment_timestamp = IntegerField(
        constraints=[SQL("DEFAULT 0")], index=True
    )
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    sticky = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tid = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_forum_index"
        indexes = (
            (("nid", "tid", "sticky", "last_comment_timestamp"), False),
        )
        primary_key = False


class History(BaseModel):
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_history"
        indexes = ((("uid", "nid"), True),)
        primary_key = CompositeKey("nid", "uid")


class HttpResponseHeaders(BaseModel):
    data = TextField(null=True)
    description = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    header = CharField(null=True)
    header_value = CharField(null=True)
    machine_name = CharField(null=True, unique=True)
    pages = TextField(null=True)
    rid = AutoField()
    roles = CharField(null=True)
    types = CharField(null=True)
    visibility = CharField(null=True)

    class Meta:
        table_name = "moov_http_response_headers"


class HybridauthIdentity(BaseModel):
    data = TextField()
    provider = CharField(constraints=[SQL("DEFAULT ''")])
    provider_identifier = CharField(constraints=[SQL("DEFAULT ''")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_hybridauth_identity"
        indexes = ((("provider", "provider_identifier"), True),)


class HybridauthSession(BaseModel):
    data = TextField()
    uid = AutoField()
    updated = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_hybridauth_session"


class ImageEffects(BaseModel):
    data = TextField()
    ieid = AutoField()
    isid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    name = CharField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_image_effects"


class ImageStyles(BaseModel):
    isid = AutoField()
    label = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(unique=True)

    class Meta:
        table_name = "moov_image_styles"


class JobSchedule(BaseModel):
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    crontab = CharField(constraints=[SQL("DEFAULT ''")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_id = AutoField()
    last = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    next = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    period = IntegerField(constraints=[SQL("DEFAULT 0")])
    periodic = IntegerField(constraints=[SQL("DEFAULT 0")])
    scheduled = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_job_schedule"
        indexes = (
            (("name", "type"), False),
            (("name", "type", "id"), False),
        )


class JobSchedulerTrigger(BaseModel):
    crontab = CharField(constraints=[SQL("DEFAULT ''")])
    hook = CharField(constraints=[SQL("DEFAULT ''")])
    last = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    trid = AutoField()

    class Meta:
        table_name = "moov_job_scheduler_trigger"


class L10NUpdateFile(BaseModel):
    filename = CharField(constraints=[SQL("DEFAULT ''")])
    fileurl = CharField(constraints=[SQL("DEFAULT ''")])
    language = CharField()
    last_checked = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    project = CharField()
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    type = CharField(constraints=[SQL("DEFAULT ''")])
    uri = CharField(constraints=[SQL("DEFAULT ''")])
    version = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_l10n_update_file"
        indexes = ((("project", "language"), True),)
        primary_key = CompositeKey("language", "project")


class L10NUpdateProject(BaseModel):
    core = CharField(constraints=[SQL("DEFAULT ''")])
    l10n_path = CharField(constraints=[SQL("DEFAULT ''")])
    l10n_server = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(primary_key=True)
    project_type = CharField()
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    version = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_l10n_update_project"


class Languages(BaseModel):
    direction = IntegerField(constraints=[SQL("DEFAULT 0")])
    domain = CharField(constraints=[SQL("DEFAULT ''")])
    enabled = IntegerField(constraints=[SQL("DEFAULT 0")])
    formula = CharField(constraints=[SQL("DEFAULT ''")])
    javascript = CharField(constraints=[SQL("DEFAULT ''")])
    language = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    name = CharField(constraints=[SQL("DEFAULT ''")])
    native = CharField(constraints=[SQL("DEFAULT ''")])
    plurals = IntegerField(constraints=[SQL("DEFAULT 0")])
    prefix = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_languages"
        indexes = ((("weight", "name"), False),)


class LinkedinToken(BaseModel):
    token_key = CharField(index=True)
    token_secret = CharField()
    type = CharField()
    uid = AutoField()

    class Meta:
        table_name = "moov_linkedin_token"


class LocalesSource(BaseModel):
    context = CharField(constraints=[SQL("DEFAULT ''")])
    lid = AutoField()
    location = TextField(null=True)
    source = TextField()
    textgroup = CharField(constraints=[SQL("DEFAULT 'default'")])
    version = CharField(constraints=[SQL("DEFAULT 'none'")])

    class Meta:
        table_name = "moov_locales_source"
        indexes = ((("source", "context"), False),)


class LocalesTarget(BaseModel):
    l10n_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    language = CharField(constraints=[SQL("DEFAULT ''")])
    lid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    plid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    plural = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    translation = TextField()

    class Meta:
        table_name = "moov_locales_target"
        indexes = ((("language", "lid", "plural"), True),)
        primary_key = CompositeKey("language", "lid", "plural")


class LoginDestination(BaseModel):
    destination = TextField()
    destination_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    enabled = IntegerField(constraints=[SQL("DEFAULT 1")])
    pages = TextField()
    pages_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    roles = TextField()
    triggers = TextField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_login_destination"


class LsAnsw(BaseModel):
    ls_aid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ls_lang = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    ls_last_import = IntegerField(constraints=[SQL("DEFAULT 0")])
    ls_sid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ls_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ls_sync = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ls_token = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = "moov_ls_answ"
        indexes = ((("nid", "ls_sid", "ls_aid"), False),)
        primary_key = False


class LsSurvey(BaseModel):
    ls_lang = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    ls_orig_type = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    ls_sid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = "moov_ls_survey"
        indexes = ((("nid", "ls_sid"), False),)
        primary_key = False


class MenuCustom(BaseModel):
    description = TextField(null=True)
    menu_name = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    title = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_menu_custom"


class MenuLinks(BaseModel):
    customized = IntegerField(constraints=[SQL("DEFAULT 0")])
    depth = IntegerField(constraints=[SQL("DEFAULT 0")])
    expanded = IntegerField(constraints=[SQL("DEFAULT 0")])
    external = IntegerField(constraints=[SQL("DEFAULT 0")])
    has_children = IntegerField(constraints=[SQL("DEFAULT 0")])
    hidden = IntegerField(constraints=[SQL("DEFAULT 0")])
    link_path = CharField(constraints=[SQL("DEFAULT ''")])
    link_title = CharField(constraints=[SQL("DEFAULT ''")])
    menu_name = CharField(constraints=[SQL("DEFAULT ''")])
    mlid = AutoField()
    module = CharField(constraints=[SQL("DEFAULT 'system'")])
    options = TextField(null=True)
    p1 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p2 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p3 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p4 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p5 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p6 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p7 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p8 = IntegerField(constraints=[SQL("DEFAULT 0")])
    p9 = IntegerField(constraints=[SQL("DEFAULT 0")])
    plid = IntegerField(constraints=[SQL("DEFAULT 0")])
    router_path = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    updated = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_menu_links"
        indexes = (
            (("link_path", "menu_name"), False),
            (
                (
                    "menu_name",
                    "p1",
                    "p2",
                    "p3",
                    "p4",
                    "p5",
                    "p6",
                    "p7",
                    "p8",
                    "p9",
                ),
                False,
            ),
            (("menu_name", "plid", "expanded", "has_children"), False),
        )


class MenuLinksVisibilityRole(BaseModel):
    mlid = IntegerField()
    rid = IntegerField(index=True)

    class Meta:
        table_name = "moov_menu_links_visibility_role"
        indexes = ((("mlid", "rid"), True),)
        primary_key = CompositeKey("mlid", "rid")


class MenuRouter(BaseModel):
    access_arguments = TextField(null=True)
    access_callback = CharField(constraints=[SQL("DEFAULT ''")])
    context = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_callback = CharField(constraints=[SQL("DEFAULT ''")])
    description = TextField()
    fit = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    include_file = TextField(null=True)
    load_functions = TextField()
    number_parts = IntegerField(constraints=[SQL("DEFAULT 0")])
    page_arguments = TextField(null=True)
    page_callback = CharField(constraints=[SQL("DEFAULT ''")])
    path = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    position = CharField(constraints=[SQL("DEFAULT ''")])
    tab_parent = CharField(constraints=[SQL("DEFAULT ''")])
    tab_root = CharField(constraints=[SQL("DEFAULT ''")])
    theme_arguments = CharField(constraints=[SQL("DEFAULT ''")])
    theme_callback = CharField(constraints=[SQL("DEFAULT ''")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    title_arguments = CharField(constraints=[SQL("DEFAULT ''")])
    title_callback = CharField(constraints=[SQL("DEFAULT ''")])
    to_arg_functions = TextField()
    type = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_menu_router"
        indexes = (
            (("tab_parent", "weight", "title"), False),
            (("tab_root", "weight", "title"), False),
        )


class Metatag(BaseModel):
    data = TextField()
    entity_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_type = CharField(constraints=[SQL("DEFAULT ''")])
    language = CharField(constraints=[SQL("DEFAULT ''")])
    revision_id = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_metatag"
        indexes = (
            (("entity_type", "entity_id", "revision_id", "language"), True),
            (("entity_type", "revision_id"), False),
        )
        primary_key = CompositeKey(
            "entity_id", "entity_type", "language", "revision_id"
        )


class MetatagConfig(BaseModel):
    cid = AutoField()
    config = TextField()
    instance = CharField(constraints=[SQL("DEFAULT ''")], unique=True)

    class Meta:
        table_name = "moov_metatag_config"


class Node(BaseModel):
    nid = AutoField()
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    vid = IntegerField(null=True, unique=True)
    tnid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    changed = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    comment = IntegerField(constraints=[SQL("DEFAULT 0")])
    created = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    language = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    promote = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    sticky = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    translate = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_node"
        indexes = (
            (("promote", "status", "sticky", "created"), False),
            (("status", "type", "nid"), False),
            (("title", "type"), False),
        )

    def get_field(self, table):
        row = table.get_or_none(table.entity_id == self.nid)

        table_name = table._meta.table_name.split("moov_field_data_", 1)[1]
        if (
            table_name == "field_type_actualite"
            or table_name == "field_type_tendance"
        ):
            column_name = f"{table_name}_tid"
        else:
            column_name = f"{table_name}_value"
        return getattr(row, column_name, None)

    def get_collection(self, table, from_table, column_name):
        entity_id = self.get_field(table)
        rows = from_table.select().where(from_table.entity_id == entity_id)

        for row in rows:
            yield getattr(row, column_name, None)

    def get_media(self, table, from_table, column_name):
        fids = self.get_collection(table, from_table, column_name)

        for fid in fids:
            media = FileManaged.get_or_none(FileManaged.fid == fid)
            yield media.uri.split("public://", 1)[1]


class NodeAccess(BaseModel):
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    gid = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_delete = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_update = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_view = IntegerField(constraints=[SQL("DEFAULT 0")])
    realm = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_node_access"
        indexes = ((("nid", "gid", "realm"), True),)
        primary_key = CompositeKey("gid", "nid", "realm")


class NodeCommentStatistics(BaseModel):
    nid = AutoField()
    cid = IntegerField(constraints=[SQL("DEFAULT 0")])
    comment_count = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    last_comment_name = CharField(null=True)
    last_comment_timestamp = IntegerField(
        constraints=[SQL("DEFAULT 0")], index=True
    )
    last_comment_uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_node_comment_statistics"


class NodeLimit(BaseModel):
    lid = AutoField()
    nlimit = IntegerField(constraints=[SQL("DEFAULT -1")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    type = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_node_limit"


class NodeLimitInterval(BaseModel):
    lid = AutoField()
    ninterval = IntegerField()
    unit = IntegerField()

    class Meta:
        table_name = "moov_node_limit_interval"


class NodeLimitRole(BaseModel):
    lid = IntegerField()
    rid = IntegerField()

    class Meta:
        table_name = "moov_node_limit_role"
        indexes = ((("lid", "rid"), True),)
        primary_key = CompositeKey("lid", "rid")


class NodeLimitType(BaseModel):
    lid = IntegerField()
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_node_limit_type"
        indexes = ((("lid", "type"), True),)
        primary_key = CompositeKey("lid", "type")


class NodeLimitUser(BaseModel):
    lid = IntegerField()
    uid = IntegerField()

    class Meta:
        table_name = "moov_node_limit_user"
        indexes = ((("lid", "uid"), True),)
        primary_key = CompositeKey("lid", "uid")


class NodeLimitUserofrole(BaseModel):
    lid = IntegerField()
    rid = IntegerField()

    class Meta:
        table_name = "moov_node_limit_userofrole"
        indexes = ((("lid", "rid"), True),)
        primary_key = CompositeKey("lid", "rid")


class NodeRevision(BaseModel):
    comment = IntegerField(constraints=[SQL("DEFAULT 0")])
    log = TextField()
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    promote = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    sticky = IntegerField(constraints=[SQL("DEFAULT 0")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    vid = AutoField()

    class Meta:
        table_name = "moov_node_revision"


class NodeType(BaseModel):
    base = CharField()
    custom = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField()
    disabled = IntegerField(constraints=[SQL("DEFAULT 0")])
    has_title = IntegerField()
    help = TextField()
    locked = IntegerField(constraints=[SQL("DEFAULT 0")])
    modified = IntegerField(constraints=[SQL("DEFAULT 0")])
    module = CharField()
    name = CharField(constraints=[SQL("DEFAULT ''")])
    orig_type = CharField(constraints=[SQL("DEFAULT ''")])
    title_label = CharField(constraints=[SQL("DEFAULT ''")])
    type = CharField(primary_key=True)

    class Meta:
        table_name = "moov_node_type"


class Nodeblock(BaseModel):
    block_title = CharField(constraints=[SQL("DEFAULT ''")])
    comment_link = CharField(constraints=[SQL("DEFAULT '0'")])
    enabled = IntegerField(constraints=[SQL("DEFAULT 1")])
    machine_name = CharField(unique=True)
    nid = AutoField()
    node_link = CharField(constraints=[SQL("DEFAULT '0'")])
    translation_fallback = IntegerField(constraints=[SQL("DEFAULT 0")])
    view_mode = CharField()

    class Meta:
        table_name = "moov_nodeblock"


class Note(BaseModel):
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    modified = IntegerField(constraints=[SQL("DEFAULT 0")])
    note = TextField(null=True)
    subject = CharField()
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_note"


class OauthCommonConsumer(BaseModel):
    configuration = TextField()
    consumer_key = TextField()
    csid = AutoField()
    key_hash = CharField(index=True)
    secret = TextField()

    class Meta:
        table_name = "moov_oauth_common_consumer"


class OauthCommonContext(BaseModel):
    authorization_levels = TextField()
    authorization_options = TextField()
    cid = AutoField()
    name = CharField(unique=True)
    title = CharField()

    class Meta:
        table_name = "moov_oauth_common_context"


class OauthCommonNonce(BaseModel):
    nonce = CharField(primary_key=True)
    timestamp = IntegerField()
    token_key = CharField()

    class Meta:
        table_name = "moov_oauth_common_nonce"
        indexes = ((("timestamp", "token_key"), False),)


class OauthCommonProviderConsumer(BaseModel):
    callback_url = CharField(constraints=[SQL("DEFAULT ''")])
    changed = IntegerField(constraints=[SQL("DEFAULT 0")])
    consumer_key = CharField(primary_key=True)
    context = CharField(constraints=[SQL("DEFAULT ''")])
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    csid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True, unique=True)
    name = CharField()
    uid = IntegerField(index=True)

    class Meta:
        table_name = "moov_oauth_common_provider_consumer"


class OauthCommonProviderToken(BaseModel):
    authorized = IntegerField(constraints=[SQL("DEFAULT 0")])
    changed = IntegerField(constraints=[SQL("DEFAULT 0")])
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    services = TextField(null=True)
    tid = IntegerField(constraints=[SQL("DEFAULT 0")], null=True, unique=True)
    token_key = CharField(primary_key=True)

    class Meta:
        table_name = "moov_oauth_common_provider_token"


class OauthCommonToken(BaseModel):
    callback_url = CharField()
    csid = IntegerField(constraints=[SQL("DEFAULT 0")])
    expires = IntegerField(constraints=[SQL("DEFAULT 0")])
    key_hash = CharField(index=True)
    secret = TextField()
    tid = AutoField()
    token_key = TextField()
    type = IntegerField(constraints=[SQL("DEFAULT 1")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_oauth_common_token"


class OneallSocialLoginIdentities(BaseModel):
    aid = IntegerField(index=True)
    identity_token = CharField(index=True)
    oasliid = AutoField()
    provider_name = CharField()

    class Meta:
        table_name = "moov_oneall_social_login_identities"


class OneallSocialLoginSettings(BaseModel):
    oaslsid = AutoField()
    setting = CharField(index=True)
    value = CharField()

    class Meta:
        table_name = "moov_oneall_social_login_settings"


class OpengraphMeta(BaseModel):
    description = TextField()
    image = CharField(constraints=[SQL("DEFAULT ''")])
    nid = AutoField()
    optional = TextField(null=True)
    title = CharField(constraints=[SQL("DEFAULT ''")])
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_opengraph_meta"


class PageManagerHandlers(BaseModel):
    conf = TextField()
    did = AutoField()
    handler = CharField(null=True)
    name = CharField(null=True, unique=True)
    subtask = CharField(constraints=[SQL("DEFAULT ''")])
    task = CharField(null=True)
    weight = IntegerField(null=True)

    class Meta:
        table_name = "moov_page_manager_handlers"
        indexes = ((("task", "subtask", "weight"), False),)


class PageManagerPages(BaseModel):
    access = TextField()
    admin_description = TextField(null=True)
    admin_title = CharField(null=True)
    arguments = TextField()
    conf = TextField()
    menu = TextField()
    name = CharField(null=True, unique=True)
    path = CharField(null=True)
    pid = AutoField()
    task = CharField(
        constraints=[SQL("DEFAULT 'page'")], index=True, null=True
    )

    class Meta:
        table_name = "moov_page_manager_pages"


class PageManagerWeights(BaseModel):
    name = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    weight = IntegerField(null=True)

    class Meta:
        table_name = "moov_page_manager_weights"
        indexes = ((("name", "weight"), False),)


class PathBreadcrumbs(BaseModel):
    data = TextField()
    machine_name = CharField(unique=True)
    name = CharField()
    path = CharField()
    path_id = AutoField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_path_breadcrumbs"


class PmIndex(BaseModel):
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_new = IntegerField(constraints=[SQL("DEFAULT 1")])
    mid = IntegerField()
    recipient = IntegerField()
    thread_id = IntegerField()
    type = CharField(constraints=[SQL("DEFAULT 'user'")])

    class Meta:
        table_name = "moov_pm_index"
        indexes = (
            (("mid", "recipient", "type"), False),
            (("mid", "recipient", "type"), True),
            (("recipient", "type", "deleted", "is_new"), False),
            (("thread_id", "recipient", "type", "deleted"), False),
        )
        primary_key = CompositeKey("mid", "recipient", "type")


class PmMessage(BaseModel):
    author = IntegerField()
    body = TextField()
    format = CharField(null=True)
    has_tokens = IntegerField(constraints=[SQL("DEFAULT 0")])
    mid = AutoField()
    reply_to_mid = IntegerField(constraints=[SQL("DEFAULT 0")])
    subject = CharField()
    timestamp = IntegerField()

    class Meta:
        table_name = "moov_pm_message"


class PmSetting(BaseModel):
    id = IntegerField()
    setting = CharField()
    type = CharField()
    value = IntegerField(null=True)

    class Meta:
        table_name = "moov_pm_setting"
        indexes = ((("id", "type", "setting"), True),)
        primary_key = CompositeKey("id", "setting", "type")


class PmTags(BaseModel):
    hidden = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    public = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tag = CharField()
    tag_id = AutoField()

    class Meta:
        table_name = "moov_pm_tags"
        indexes = ((("tag_id", "tag", "public"), False),)


class PmTagsIndex(BaseModel):
    tag_id = IntegerField()
    thread_id = IntegerField()
    uid = IntegerField()

    class Meta:
        table_name = "moov_pm_tags_index"
        indexes = (
            (("tag_id", "uid", "thread_id"), True),
            (("uid", "thread_id"), False),
        )
        primary_key = CompositeKey("tag_id", "thread_id", "uid")


class Poll(BaseModel):
    active = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = AutoField()
    runtime = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_poll"


class PollChoice(BaseModel):
    chid = AutoField()
    chtext = CharField(constraints=[SQL("DEFAULT ''")])
    chvotes = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_poll_choice"


class PollVote(BaseModel):
    chid = IntegerField(index=True)
    hostname = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    nid = IntegerField()
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_poll_vote"
        indexes = ((("nid", "uid", "hostname"), True),)
        primary_key = CompositeKey("hostname", "nid", "uid")


class PrintNodeConf(BaseModel):
    comments = IntegerField(constraints=[SQL("DEFAULT 1")])
    link = IntegerField(constraints=[SQL("DEFAULT 1")])
    nid = AutoField()
    url_list = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = "moov_print_node_conf"


class PrintPageCounter(BaseModel):
    path = CharField(primary_key=True)
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    totalcount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_print_page_counter"


class PrintPdfNodeConf(BaseModel):
    comments = IntegerField(constraints=[SQL("DEFAULT 1")])
    link = IntegerField(constraints=[SQL("DEFAULT 1")])
    nid = AutoField()
    orientation = CharField(null=True)
    size = CharField(null=True)
    url_list = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = "moov_print_pdf_node_conf"


class PrintPdfPageCounter(BaseModel):
    path = CharField(primary_key=True)
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    totalcount = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_print_pdf_page_counter"


class Queue(BaseModel):
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(null=True)
    expire = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    item_id = AutoField()
    name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_queue"
        indexes = ((("name", "created"), False),)


class RdfMapping(BaseModel):
    bundle = CharField()
    mapping = TextField(null=True)
    type = CharField()

    class Meta:
        table_name = "moov_rdf_mapping"
        indexes = ((("type", "bundle"), True),)
        primary_key = CompositeKey("bundle", "type")


class Registry(BaseModel):
    filename = CharField()
    module = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(constraints=[SQL("DEFAULT ''")])
    type = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_registry"
        indexes = (
            (("name", "type"), True),
            (("type", "weight", "module"), False),
        )
        primary_key = CompositeKey("name", "type")


class RegistryFile(BaseModel):
    filename = CharField(primary_key=True)
    hash = CharField()

    class Meta:
        table_name = "moov_registry_file"


class RevisioningScheduler(BaseModel):
    revision_date = IntegerField()
    revision_nid = IntegerField()
    revision_uid = IntegerField()
    revision_vid = AutoField()

    class Meta:
        table_name = "moov_revisioning_scheduler"


class Role(BaseModel):
    name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    rid = AutoField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_role"
        indexes = ((("name", "weight"), False),)


class RolePermission(BaseModel):
    module = CharField(constraints=[SQL("DEFAULT ''")])
    permission = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    rid = IntegerField()

    class Meta:
        table_name = "moov_role_permission"
        indexes = ((("rid", "permission"), True),)
        primary_key = CompositeKey("permission", "rid")


class RulesConfig(BaseModel):
    access_exposed = IntegerField(constraints=[SQL("DEFAULT 0")])
    active = IntegerField(constraints=[SQL("DEFAULT 1")])
    data = TextField(null=True)
    dirty = IntegerField(constraints=[SQL("DEFAULT 0")])
    label = CharField(constraints=[SQL("DEFAULT 'unlabeled'")])
    module = CharField(null=True)
    name = CharField(unique=True)
    owner = CharField(constraints=[SQL("DEFAULT 'rules'")])
    plugin = CharField(index=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_rules_config"


class RulesDependencies(BaseModel):
    id = IntegerField()
    module = CharField(index=True)

    class Meta:
        table_name = "moov_rules_dependencies"
        indexes = ((("id", "module"), True),)
        primary_key = CompositeKey("id", "module")


class RulesScheduler(BaseModel):
    config = CharField(constraints=[SQL("DEFAULT ''")])
    data = TextField(null=True)
    date = IntegerField(index=True)
    handler = CharField(null=True)
    identifier = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    tid = AutoField()

    class Meta:
        table_name = "moov_rules_scheduler"


class RulesTags(BaseModel):
    id = IntegerField()
    tag = CharField()

    class Meta:
        table_name = "moov_rules_tags"
        indexes = ((("id", "tag"), True),)
        primary_key = CompositeKey("id", "tag")


class RulesTrigger(BaseModel):
    event = CharField(constraints=[SQL("DEFAULT ''")])
    id = IntegerField()

    class Meta:
        table_name = "moov_rules_trigger"
        indexes = ((("id", "event"), True),)
        primary_key = CompositeKey("event", "id")


class Scheduler(BaseModel):
    nid = AutoField()
    publish_on = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    unpublish_on = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_scheduler"


class SearchDataset(BaseModel):
    data = TextField()
    reindex = IntegerField(constraints=[SQL("DEFAULT 0")])
    sid = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField()

    class Meta:
        table_name = "moov_search_dataset"
        indexes = ((("sid", "type"), True),)
        primary_key = CompositeKey("sid", "type")


class SearchIndex(BaseModel):
    score = FloatField(null=True)
    sid = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField()
    word = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_search_index"
        indexes = (
            (("sid", "type"), False),
            (("word", "sid", "type"), True),
        )
        primary_key = CompositeKey("sid", "type", "word")


class SearchNodeLinks(BaseModel):
    caption = TextField(null=True)
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sid = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_search_node_links"
        indexes = ((("sid", "type", "nid"), True),)
        primary_key = CompositeKey("nid", "sid", "type")


class SearchTotal(BaseModel):
    count = FloatField(null=True)
    word = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)

    class Meta:
        table_name = "moov_search_total"


class Semaphore(BaseModel):
    expire = FloatField(index=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    value = CharField(constraints=[SQL("DEFAULT ''")], index=True)

    class Meta:
        table_name = "moov_semaphore"


class Sequences(BaseModel):
    value = AutoField()

    class Meta:
        table_name = "moov_sequences"


class ServicesEndpoint(BaseModel):
    authentication = TextField()
    debug = IntegerField(constraints=[SQL("DEFAULT 0")])
    eid = AutoField()
    name = CharField(unique=True)
    path = CharField()
    resources = TextField()
    server = CharField()
    server_settings = TextField()

    class Meta:
        table_name = "moov_services_endpoint"


class ServicesUser(BaseModel):
    changed = IntegerField(constraints=[SQL("DEFAULT 0")])
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField()

    class Meta:
        table_name = "moov_services_user"
        primary_key = False


class Sessions(BaseModel):
    cache = IntegerField(constraints=[SQL("DEFAULT 0")])
    hostname = CharField(constraints=[SQL("DEFAULT ''")])
    session = TextField(null=True)
    sid = CharField()
    ssid = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    uid = IntegerField(index=True)

    class Meta:
        table_name = "moov_sessions"
        indexes = ((("sid", "ssid"), True),)
        primary_key = CompositeKey("sid", "ssid")


class ShortcutSet(BaseModel):
    set_name = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    title = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_shortcut_set"


class ShortcutSetUsers(BaseModel):
    set_name = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    uid = AutoField()

    class Meta:
        table_name = "moov_shortcut_set_users"


class SmartIp(BaseModel):
    city = CharField(null=True)
    country_code = CharField()
    geoip_id = BigIntegerField(index=True)
    ip_ref = BigAutoField()
    latitude = FloatField()
    longitude = FloatField()
    region = CharField(null=True)
    zip = CharField(null=True)

    class Meta:
        table_name = "moov_smart_ip"


class SocialShareNetworks(BaseModel):
    human_name = CharField(null=True)
    locked = IntegerField(constraints=[SQL("DEFAULT 0")])
    machine_name = CharField(primary_key=True)
    url = TextField(null=True)
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_social_share_networks"


class Survey(BaseModel):
    created = IntegerField()
    fields = TextField()
    module = CharField(null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    pid = AutoField()
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    title = CharField(constraints=[SQL("DEFAULT ''")])
    type = CharField(constraints=[SQL("DEFAULT ''")])
    uid = IntegerField()

    class Meta:
        table_name = "moov_survey"


class SurveyQuestion(BaseModel):
    created = IntegerField()
    field = TextField()
    label = TextField()
    module = CharField(null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    pid = AutoField()
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    type = CharField(constraints=[SQL("DEFAULT ''")])
    uid = IntegerField()

    class Meta:
        table_name = "moov_survey_question"


class SurveyQuestionResponse(BaseModel):
    created = IntegerField()
    pid = AutoField()
    question_id = IntegerField(index=True)
    question_key = CharField()
    score = IntegerField(null=True)
    survey_response_id = IntegerField()
    value = TextField()
    value_key = CharField(null=True)

    class Meta:
        table_name = "moov_survey_question_response"
        indexes = ((("survey_response_id", "question_key"), False),)


class SurveyResponse(BaseModel):
    created = IntegerField()
    pid = AutoField()
    score = IntegerField(null=True)
    survey_id = IntegerField(index=True)
    uid = IntegerField(index=True)

    class Meta:
        table_name = "moov_survey_response"


class System(BaseModel):
    bootstrap = IntegerField(constraints=[SQL("DEFAULT 0")])
    filename = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    info = TextField(null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")])
    owner = CharField(constraints=[SQL("DEFAULT ''")])
    schema_version = IntegerField(constraints=[SQL("DEFAULT -1")])
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_system"
        indexes = (
            (("status", "bootstrap", "type", "weight", "name"), False),
            (("type", "name"), False),
        )


class TaxonomyAccessDefault(BaseModel):
    grant_create = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_delete = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_list = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_update = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_view = IntegerField(constraints=[SQL("DEFAULT 0")])
    rid = IntegerField(constraints=[SQL("DEFAULT 0")])
    vid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_taxonomy_access_default"
        indexes = ((("vid", "rid"), True),)
        primary_key = CompositeKey("rid", "vid")


class TaxonomyAccessTerm(BaseModel):
    grant_create = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_delete = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_list = IntegerField(constraints=[SQL("DEFAULT 1")])
    grant_update = IntegerField(constraints=[SQL("DEFAULT 0")])
    grant_view = IntegerField(constraints=[SQL("DEFAULT 0")])
    rid = IntegerField(constraints=[SQL("DEFAULT 0")])
    tid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_taxonomy_access_term"
        indexes = ((("tid", "rid"), True),)
        primary_key = CompositeKey("rid", "tid")


class TaxonomyBreadcrumbTerm(BaseModel):
    path = CharField()
    tid = AutoField()

    class Meta:
        table_name = "moov_taxonomy_breadcrumb_term"


class TaxonomyBreadcrumbVocabulary(BaseModel):
    path = CharField()
    vid = AutoField()

    class Meta:
        table_name = "moov_taxonomy_breadcrumb_vocabulary"


class TaxonomyIndex(BaseModel):
    created = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sticky = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    tid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_taxonomy_index"
        indexes = ((("tid", "sticky", "created"), False),)
        primary_key = False


class TaxonomyMenu(BaseModel):
    mlid = IntegerField(constraints=[SQL("DEFAULT 0")])
    tid = IntegerField(constraints=[SQL("DEFAULT 0")])
    vid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_taxonomy_menu"
        indexes = ((("mlid", "tid"), True),)
        primary_key = CompositeKey("mlid", "tid")


class TaxonomyTermData(BaseModel):
    tid = AutoField()
    vid = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = TextField(null=True)
    format = CharField(null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_taxonomy_term_data"
        indexes = (
            (("vid", "name"), False),
            (("vid", "weight", "name"), False),
        )


class TaxonomyTermHierarchy(BaseModel):
    parent = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    tid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_taxonomy_term_hierarchy"
        indexes = ((("tid", "parent"), True),)
        primary_key = CompositeKey("parent", "tid")


class TaxonomyVocabulary(BaseModel):
    vid = AutoField()
    name = CharField(constraints=[SQL("DEFAULT ''")])
    machine_name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    description = TextField(null=True)
    hierarchy = IntegerField(constraints=[SQL("DEFAULT 0")])
    module = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_taxonomy_vocabulary"
        indexes = ((("weight", "name"), False),)


class Termstatus(BaseModel):
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    tid = AutoField()

    class Meta:
        table_name = "moov_termstatus"


class TriggerAssignments(BaseModel):
    aid = CharField(constraints=[SQL("DEFAULT ''")])
    hook = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_trigger_assignments"
        indexes = ((("hook", "aid"), True),)
        primary_key = CompositeKey("aid", "hook")


class UrlAlias(BaseModel):
    alias = CharField(constraints=[SQL("DEFAULT ''")])
    language = CharField(constraints=[SQL("DEFAULT ''")])
    pid = AutoField()
    source = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_url_alias"
        indexes = (
            (("alias", "language", "pid"), False),
            (("source", "language", "pid"), False),
        )


class UserEmailVerification(BaseModel):
    uid = AutoField()
    verified = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_user_email_verification"


class UserImport(BaseModel):
    auto_import_directory = CharField(constraints=[SQL("DEFAULT ''")])
    field_match = TextField()
    filename = CharField(constraints=[SQL("DEFAULT ''")])
    filepath = TextField()
    import_id = AutoField()
    name = CharField(constraints=[SQL("DEFAULT ''")])
    oldfilename = CharField(constraints=[SQL("DEFAULT ''")])
    options = TextField()
    pointer = IntegerField(constraints=[SQL("DEFAULT 0")])
    processed = IntegerField(constraints=[SQL("DEFAULT 0")])
    roles = TextField()
    setting = CharField(constraints=[SQL("DEFAULT ''")])
    started = IntegerField(constraints=[SQL("DEFAULT 0")])
    valid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_user_import"


class UserImportErrors(BaseModel):
    data = TextField()
    errors = TextField()
    import_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = "moov_user_import_errors"
        primary_key = False


class UserVerify(BaseModel):
    code = CharField(null=True)
    errors = IntegerField(constraints=[SQL("DEFAULT 0")])
    expires = IntegerField(null=True)
    mail_success = IntegerField(null=True)
    uid = IntegerField(unique=True)

    class Meta:
        table_name = "moov_user_verify"
        primary_key = False


class Users(BaseModel):
    access = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    created = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    data = TextField(null=True)
    init = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    language = CharField(constraints=[SQL("DEFAULT ''")])
    login = IntegerField(constraints=[SQL("DEFAULT 0")])
    mail = CharField(constraints=[SQL("DEFAULT ''")], index=True, null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    pass_ = CharField(column_name="pass", constraints=[SQL("DEFAULT ''")])
    picture = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    signature = CharField(constraints=[SQL("DEFAULT ''")])
    signature_format = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 0")])
    theme = CharField(constraints=[SQL("DEFAULT ''")])
    timezone = CharField(null=True)
    uid = AutoField()

    class Meta:
        table_name = "moov_users"


class UsersRoles(BaseModel):
    rid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_users_roles"
        indexes = ((("uid", "rid"), True),)
        primary_key = CompositeKey("rid", "uid")


class Variable(BaseModel):
    name = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    value = TextField()

    class Meta:
        table_name = "moov_variable"


class ViewsDisplay(BaseModel):
    display_options = TextField(null=True)
    display_plugin = CharField(constraints=[SQL("DEFAULT ''")])
    display_title = CharField(constraints=[SQL("DEFAULT ''")])
    id = CharField(constraints=[SQL("DEFAULT ''")])
    position = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    vid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_views_display"
        indexes = (
            (("vid", "id"), True),
            (("vid", "position"), False),
        )
        primary_key = CompositeKey("id", "vid")


class ViewsView(BaseModel):
    base_table = CharField(constraints=[SQL("DEFAULT ''")])
    core = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    description = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    human_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    name = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    tag = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    vid = AutoField()

    class Meta:
        table_name = "moov_views_view"


class VlsRooms(BaseModel):
    advancedcamsettings = IntegerField(constraints=[SQL("DEFAULT 1")])
    bandwidth = IntegerField(constraints=[SQL("DEFAULT 40960")])
    camfps = IntegerField(constraints=[SQL("DEFAULT 15")])
    camheight = IntegerField(constraints=[SQL("DEFAULT 240")])
    camwidth = IntegerField(constraints=[SQL("DEFAULT 320")])
    configuresource = IntegerField(constraints=[SQL("DEFAULT 1")])
    credits = IntegerField(constraints=[SQL("DEFAULT 0")])
    enabledchat = IntegerField(constraints=[SQL("DEFAULT 1")])
    enabledusers = IntegerField(constraints=[SQL("DEFAULT 1")])
    enabledvideo = IntegerField(constraints=[SQL("DEFAULT 1")])
    fillwindow = IntegerField(constraints=[SQL("DEFAULT 1")])
    filterregex = CharField(
        constraints=[SQL("DEFAULT '(?i)(fuck|cunt)(?-i)'")], null=True
    )
    filterreplace = CharField(constraints=[SQL("DEFAULT ' ** '")], null=True)
    floodprotection = IntegerField(constraints=[SQL("DEFAULT 3")])
    floodprotection2 = IntegerField(constraints=[SQL("DEFAULT 3")])
    labelcolor = CharField(constraints=[SQL("DEFAULT 'FFFFFF'")], null=True)
    layoutcode = TextField(null=True)
    maxbandwidth = IntegerField(constraints=[SQL("DEFAULT 81920")])
    micrate = IntegerField(constraints=[SQL("DEFAULT 22")])
    nid = IntegerField(index=True)
    noembeds = IntegerField(constraints=[SQL("DEFAULT 0")])
    offlinemessage = TextField(null=True)
    onlyvideo = IntegerField(constraints=[SQL("DEFAULT 0")])
    room = CharField(index=True, null=True)
    room_limit = IntegerField(constraints=[SQL("DEFAULT 50")])
    showtimer = IntegerField(constraints=[SQL("DEFAULT 1")])
    timecreated = IntegerField(constraints=[SQL("DEFAULT 0")])
    timeexpire = IntegerField(constraints=[SQL("DEFAULT 0")])
    timelastaccess = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    timeout = IntegerField(constraints=[SQL("DEFAULT 0")])
    timeused = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    vid = IntegerField()
    visitors = IntegerField(constraints=[SQL("DEFAULT 1")])
    welcome = TextField(null=True)
    welcome2 = TextField(null=True)
    write_text = IntegerField(constraints=[SQL("DEFAULT 1")])
    write_text2 = IntegerField(constraints=[SQL("DEFAULT 1")])

    class Meta:
        table_name = "moov_vls_rooms"
        indexes = ((("vid", "nid"), True),)
        primary_key = CompositeKey("nid", "vid")


class VotingapiCache(BaseModel):
    entity_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_type = CharField(constraints=[SQL("DEFAULT 'node'")])
    function = CharField(constraints=[SQL("DEFAULT ''")])
    tag = CharField(constraints=[SQL("DEFAULT 'vote'")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    value = FloatField(constraints=[SQL("DEFAULT 0")])
    value_type = CharField(constraints=[SQL("DEFAULT 'percent'")])
    vote_cache_id = AutoField()

    class Meta:
        table_name = "moov_votingapi_cache"
        indexes = (
            (("entity_type", "entity_id"), False),
            (("entity_type", "entity_id", "function"), False),
            (("entity_type", "entity_id", "tag", "function"), False),
            (("entity_type", "entity_id", "value_type", "tag"), False),
            (
                ("entity_type", "entity_id", "value_type", "tag", "function"),
                False,
            ),
        )


class VotingapiVote(BaseModel):
    entity_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    entity_type = CharField(constraints=[SQL("DEFAULT 'node'")])
    tag = CharField(constraints=[SQL("DEFAULT 'vote'")])
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])
    value = FloatField(constraints=[SQL("DEFAULT 0")])
    value_type = CharField(constraints=[SQL("DEFAULT 'percent'")])
    vote_id = AutoField()
    vote_source = CharField(null=True)

    class Meta:
        table_name = "moov_votingapi_vote"
        indexes = (
            (("entity_type", "entity_id", "uid"), False),
            (("entity_type", "entity_id", "value_type", "tag"), False),
            (("entity_type", "entity_id", "vote_source"), False),
            (("entity_type", "uid"), False),
        )


class Watchdog(BaseModel):
    hostname = CharField(constraints=[SQL("DEFAULT ''")])
    link = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    location = TextField()
    message = TextField()
    referer = TextField(null=True)
    severity = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    timestamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    uid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    variables = TextField()
    wid = AutoField()

    class Meta:
        table_name = "moov_watchdog"


class WeatherDisplays(BaseModel):
    config = TextField()
    number = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_weather_displays"
        indexes = ((("type", "number"), True),)
        primary_key = CompositeKey("number", "type")


class WeatherDisplaysPlaces(BaseModel):
    display_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    display_type = CharField(constraints=[SQL("DEFAULT ''")])
    displayed_name = CharField(null=True)
    place_geoid = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_weather_displays_places"


class WeatherForecastInformation(BaseModel):
    geoid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    last_update = CharField(constraints=[SQL("DEFAULT ''")])
    next_download_attempt = CharField(constraints=[SQL("DEFAULT ''")])
    next_update = CharField(constraints=[SQL("DEFAULT ''")])
    utc_offset = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_weather_forecast_information"


class WeatherForecasts(BaseModel):
    geoid = CharField(constraints=[SQL("DEFAULT ''")])
    period = CharField(constraints=[SQL("DEFAULT ''")])
    precipitation = FloatField(null=True)
    pressure = IntegerField(null=True)
    symbol = CharField(constraints=[SQL("DEFAULT ''")])
    temperature = IntegerField(null=True)
    time_from = CharField(constraints=[SQL("DEFAULT ''")])
    time_to = CharField(constraints=[SQL("DEFAULT ''")])
    wind_direction = IntegerField(null=True)
    wind_speed = FloatField(null=True)

    class Meta:
        table_name = "moov_weather_forecasts"


class WeatherPlaces(BaseModel):
    country = CharField(constraints=[SQL("DEFAULT ''")])
    geoid = CharField(constraints=[SQL("DEFAULT ''")], primary_key=True)
    latitude = FloatField(constraints=[SQL("DEFAULT 0")])
    link = CharField(constraints=[SQL("DEFAULT ''")])
    longitude = FloatField(constraints=[SQL("DEFAULT 0")])
    name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_weather_places"


class Webform(BaseModel):
    allow_draft = IntegerField(constraints=[SQL("DEFAULT 0")])
    auto_save = IntegerField(constraints=[SQL("DEFAULT 0")])
    block = IntegerField(constraints=[SQL("DEFAULT 0")])
    confidential = IntegerField(constraints=[SQL("DEFAULT 0")])
    confirmation = TextField()
    confirmation_format = CharField(null=True)
    next_serial = IntegerField(constraints=[SQL("DEFAULT 1")])
    nid = AutoField()
    preview = IntegerField(constraints=[SQL("DEFAULT 0")])
    preview_excluded_components = TextField()
    preview_message = TextField()
    preview_message_format = CharField(null=True)
    preview_next_button_label = CharField(null=True)
    preview_prev_button_label = CharField(null=True)
    preview_title = CharField(null=True)
    progressbar_bar = IntegerField(constraints=[SQL("DEFAULT 0")])
    progressbar_include_confirmation = IntegerField(
        constraints=[SQL("DEFAULT 0")]
    )
    progressbar_label_confirmation = CharField(null=True)
    progressbar_label_first = CharField(null=True)
    progressbar_page_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    progressbar_pagebreak_labels = IntegerField(constraints=[SQL("DEFAULT 0")])
    progressbar_percent = IntegerField(constraints=[SQL("DEFAULT 0")])
    redirect_url = CharField(
        constraints=[SQL("DEFAULT '<confirmation>'")], null=True
    )
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    submit_interval = IntegerField(constraints=[SQL("DEFAULT -1")])
    submit_limit = IntegerField(constraints=[SQL("DEFAULT -1")])
    submit_notice = IntegerField(constraints=[SQL("DEFAULT 1")])
    submit_text = CharField(null=True)
    total_submit_interval = IntegerField(constraints=[SQL("DEFAULT -1")])
    total_submit_limit = IntegerField(constraints=[SQL("DEFAULT -1")])
    webform_ajax = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform"


class WebformComponent(BaseModel):
    cid = IntegerField(constraints=[SQL("DEFAULT 0")])
    extra = TextField()
    form_key = CharField(null=True)
    name = TextField()
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    pid = IntegerField(constraints=[SQL("DEFAULT 0")])
    required = IntegerField(constraints=[SQL("DEFAULT 0")])
    type = CharField(null=True)
    value = TextField()
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_component"
        indexes = ((("nid", "cid"), True),)
        primary_key = CompositeKey("cid", "nid")


class WebformConditional(BaseModel):
    andor = CharField(null=True)
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    rgid = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_conditional"
        indexes = ((("nid", "rgid"), True),)
        primary_key = CompositeKey("nid", "rgid")


class WebformConditionalActions(BaseModel):
    action = CharField(null=True)
    aid = IntegerField(constraints=[SQL("DEFAULT 0")])
    argument = TextField(null=True)
    invert = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    rgid = IntegerField(constraints=[SQL("DEFAULT 0")])
    target = CharField(null=True)
    target_type = CharField(null=True)

    class Meta:
        table_name = "moov_webform_conditional_actions"
        indexes = ((("nid", "rgid", "aid"), True),)
        primary_key = CompositeKey("aid", "nid", "rgid")


class WebformConditionalRules(BaseModel):
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    operator = CharField(null=True)
    rgid = IntegerField(constraints=[SQL("DEFAULT 0")])
    rid = IntegerField(constraints=[SQL("DEFAULT 0")])
    source = IntegerField(constraints=[SQL("DEFAULT 0")])
    source_type = CharField(null=True)
    value = TextField(null=True)

    class Meta:
        table_name = "moov_webform_conditional_rules"
        indexes = ((("nid", "rgid", "rid"), True),)
        primary_key = CompositeKey("nid", "rgid", "rid")


class WebformEmails(BaseModel):
    attachments = IntegerField(constraints=[SQL("DEFAULT 0")])
    eid = IntegerField(constraints=[SQL("DEFAULT 0")])
    email = TextField(null=True)
    exclude_empty = IntegerField(constraints=[SQL("DEFAULT 0")])
    excluded_components = TextField()
    extra = TextField()
    from_address = TextField(null=True)
    from_name = TextField(null=True)
    html = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    subject = TextField(null=True)
    template = TextField(null=True)

    class Meta:
        table_name = "moov_webform_emails"
        indexes = ((("nid", "eid"), True),)
        primary_key = CompositeKey("eid", "nid")


class WebformLastDownload(BaseModel):
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    requested = IntegerField(constraints=[SQL("DEFAULT 0")])
    sid = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_last_download"
        indexes = ((("nid", "uid"), True),)
        primary_key = CompositeKey("nid", "uid")


class WebformRegistration(BaseModel):
    account_fields = TextField(null=True)
    enabled = IntegerField(constraints=[SQL("DEFAULT 0")])
    mail = CharField(null=True)
    mail_confirm = CharField(null=True)
    name = CharField(null=True)
    nid = AutoField()
    opt_in = CharField(null=True)
    opt_in_value = CharField(null=True)
    pass_ = CharField(column_name="pass", null=True)
    pass_confirm = CharField(null=True)
    roles = TextField(null=True)
    status = IntegerField(null=True)
    theme_override = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_registration"


class WebformRoles(BaseModel):
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    rid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_roles"
        indexes = ((("nid", "rid"), True),)
        primary_key = CompositeKey("nid", "rid")


class WebformSubmissions(BaseModel):
    completed = IntegerField(constraints=[SQL("DEFAULT 0")])
    highest_valid_page = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_draft = IntegerField(constraints=[SQL("DEFAULT 0")])
    modified = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = IntegerField(constraints=[SQL("DEFAULT 0")])
    remote_addr = CharField(null=True)
    serial = IntegerField()
    sid = AutoField()
    submitted = IntegerField(constraints=[SQL("DEFAULT 0")])
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_submissions"
        indexes = (
            (("nid", "serial"), True),
            (("nid", "sid"), False),
            (("nid", "uid", "sid"), False),
            (("sid", "nid"), True),
        )


class WebformSubmittedData(BaseModel):
    cid = IntegerField(constraints=[SQL("DEFAULT 0")])
    data = TextField(index=True)
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    no = CharField(constraints=[SQL("DEFAULT '0'")])
    sid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_submitted_data"
        indexes = (
            (("nid", "sid", "cid", "no"), True),
            (("sid", "nid"), False),
        )
        primary_key = CompositeKey("cid", "nid", "no", "sid")


class WebformValidationRule(BaseModel):
    data = TextField(null=True)
    error_message = TextField(null=True)
    negate = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    ruleid = AutoField()
    rulename = CharField(constraints=[SQL("DEFAULT ''")])
    validator = CharField(constraints=[SQL("DEFAULT ''")])
    weight = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_validation_rule"


class WebformValidationRuleComponents(BaseModel):
    cid = IntegerField(constraints=[SQL("DEFAULT 0")])
    ruleid = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = "moov_webform_validation_rule_components"
        indexes = ((("ruleid", "cid"), True),)
        primary_key = CompositeKey("cid", "ruleid")


class WorkbenchAccess(BaseModel):
    access_id = CharField(constraints=[SQL("DEFAULT ''")])
    access_scheme = CharField(constraints=[SQL("DEFAULT ''")])
    access_type = CharField(constraints=[SQL("DEFAULT ''")])
    access_type_id = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = "moov_workbench_access"
        indexes = ((("access_id", "access_scheme"), True),)
        primary_key = CompositeKey("access_id", "access_scheme")


class WorkbenchAccessNode(BaseModel):
    access_id = CharField(constraints=[SQL("DEFAULT ''")])
    access_scheme = CharField(constraints=[SQL("DEFAULT ''")])
    nid = IntegerField()

    class Meta:
        table_name = "moov_workbench_access_node"
        indexes = ((("nid", "access_id", "access_scheme"), True),)
        primary_key = CompositeKey("access_id", "access_scheme", "nid")


class WorkbenchAccessRole(BaseModel):
    access_id = CharField(constraints=[SQL("DEFAULT ''")])
    access_scheme = CharField(constraints=[SQL("DEFAULT ''")])
    rid = IntegerField()

    class Meta:
        table_name = "moov_workbench_access_role"
        indexes = ((("rid", "access_id", "access_scheme"), True),)
        primary_key = CompositeKey("access_id", "access_scheme", "rid")


class WorkbenchAccessUser(BaseModel):
    access_id = CharField(constraints=[SQL("DEFAULT ''")])
    access_scheme = CharField(constraints=[SQL("DEFAULT ''")])
    uid = IntegerField()

    class Meta:
        table_name = "moov_workbench_access_user"
        indexes = ((("uid", "access_id", "access_scheme"), True),)
        primary_key = CompositeKey("access_id", "access_scheme", "uid")


class WorkbenchModerationNodeHistory(BaseModel):
    hid = AutoField()
    vid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    uid = IntegerField(constraints=[SQL("DEFAULT 0")])
    from_state = CharField(null=True)
    is_current = IntegerField(constraints=[SQL("DEFAULT 0")])
    nid = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    published = IntegerField(constraints=[SQL("DEFAULT 0")])
    stamp = IntegerField(constraints=[SQL("DEFAULT 0")])
    state = CharField(null=True)

    class Meta:
        table_name = "moov_workbench_moderation_node_history"


class WorkbenchModerationStates(BaseModel):
    description = CharField(null=True)
    label = CharField(null=True)
    name = CharField(primary_key=True)
    weight = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = "moov_workbench_moderation_states"


class WorkbenchModerationTransitions(BaseModel):
    from_name = CharField(null=True)
    name = CharField(null=True)
    to_name = CharField(null=True)

    class Meta:
        table_name = "moov_workbench_moderation_transitions"
