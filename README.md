# DjangoPro
탬플릿 기본 레이아웃은 Showap에 base.html에 있습니다
탬플릿 상속을 통해서 사용하면 됩니다
{% extends 'base.html'%} 상속받는 탬플릿

{% block content%} 
이 사이에다가 탬플릿 작성하심됩니다
{% endblock%}
