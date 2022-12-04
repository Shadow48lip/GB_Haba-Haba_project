CUSTOM_CONFIGS = {
    'iframe': True,
    'summernote': {
        'airMode': False,
        'width': '80%',
        'height': '480',
        'lang': 'ru-RU',
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'underline', 'italic', 'clear']],
            ['fontname', ['fontname']],
            ['color', ['color']],
            ['table', ['table']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['insert', ['link', 'picture', 'emoji']],
            ['view', ['codeview', 'help']],
        ],
    },
    'attachment_require_authentication': True,
    'lazy': True,
    'css': (
        '../../../static/plugins/summernote/smileys/summernote-ext-emoji-ajax.css',
        '../../../static/plugins/bootstrap-icons/bootstrap-icons.css',
    ),
    'css_for_inplace': (
        '../../../static/plugins/summernote/smileys/summernote-ext-emoji-ajax.css',
        '../../../static/plugins/bootstrap-icons/bootstrap-icons.css',
    ),
    'js': (  # This is for SummernoteWidget
        '../../../static/plugins/summernote/smileys/summernote-ext-emoji-ajax.js',
    ),
    'js_for_inplace': (  # Also for SummernoteInplaceWidget
        '../../../static/plugins/summernote/smileys/summernote-ext-emoji-ajax.js',
    ),
}
