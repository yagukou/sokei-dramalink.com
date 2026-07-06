from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Performance

# 📁 1. スケジュール一覧・アーカイブ表示（編集ボタンの導線を追加）
def schedule_view(request):
    now = timezone.now()
    current_performances = Performance.objects.filter(start_date__lte=now, end_date__gte=now).order_by('start_date')
    archive_performances = Performance.objects.filter(end_date__lt=now).order_by('-end_date')
    
    return render(request, 'Schedule.html', {
        'current_performances': current_performances,
        'archive_performances': archive_performances,
    })

# ➕ 2. 新規公演の登録ページ
def add_schedule_view(request):
    if request.method == 'POST':
        Performance.objects.create(
            title=request.POST.get('title'),
            theater_group=request.POST.get('theater_group'),
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            description=request.POST.get('description')
        )
        return redirect('schedule_view')
    return render(request, 'ManageSchedule.html', {'is_edit': False})

# 📝 3. 【追加】投稿した公演の編集ページ
def edit_schedule_view(request, pk):
    # URLから渡されたID（pk）の公演データを取得。なければ404エラー
    performance = get_object_or_404(Performance, pk=pk)
    
    if request.method == 'POST':
        # フォームから送られてきたデータで上書き保存
        performance.title = request.POST.get('title')
        performance.theater_group = request.POST.get('theater_group')
        performance.start_date = request.POST.get('start_date')
        performance.end_date = request.POST.get('end_date')
        performance.description = request.POST.get('description')
        performance.save() # データベースを更新
        return redirect('schedule_view')
        
    # 編集画面を開いたときは、既存のデータをフォームに渡す
    return render(request, 'ManageSchedule.html', {
        'performance': performance,
        'is_edit': True # HTML側で「編集モード」だと判定するためのフラグ
    })