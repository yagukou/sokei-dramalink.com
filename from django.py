from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Performance  # 公演データの設計図

# 🛠️ 公演を設定・登録するための専用ページの処理
def manage_schedule_view(request):
    
    # ユーザーが「登録する」ボタンを押して、データを送ってきた場合（POST）
    if request.method == 'POST':
        # 画面の入力フォームからデータを受け取る
        title = request.POST.get('title')
        theater_group = request.POST.get('theater_group')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        
        # データベースに新しい公演情報を保存（これで自動的にアーカイブか上演中かが判別されます）
        Performance.objects.create(
            title=title,
            theater_group=theater_group,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        
        # 登録が完了したら、公演スケジュール一覧ページ（前回作ったページ）に自動で移動する
        return redirect('schedule_view')  # ※URL設定名に合わせて変更してください
        
    # 普通に「設定ページ」を開いたときは、入力用のHTMLを表示する
    return render(request, 'ManageSchedule.html')