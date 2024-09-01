from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

# タスクデータ: タスク、作成日時、期限を格納するリスト
todos = []
completed_todos = []

@app.route('/')
def index():
    current_time = datetime.now()
    # 期限切れの確認
    for todo in todos:
        deadline = datetime.strptime(todo['deadline'], '%Y-%m-%dT%H:%M')
        todo['expired'] = current_time > deadline
    return render_template('index.html', todos=todos)

@app.route('/new', methods=['GET', 'POST'])
def new_task():
    if request.method == 'POST':
        todo = request.form.get('todo')
        deadline = request.form.get('deadline')
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if todo:
            todos.append({'task': todo, 'timestamp': timestamp, 'deadline': deadline, 'expired': False})
        return redirect(url_for('index'))
    return render_template('new_task.html')

@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_task(todo_id):
    if 0 <= todo_id < len(todos):
        if request.method == 'POST':
            new_task = request.form.get('todo')
            new_deadline = request.form.get('deadline')
            todos[todo_id]['task'] = new_task
            todos[todo_id]['deadline'] = new_deadline
            todos[todo_id]['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return redirect(url_for('index'))
        return render_template('edit_task.html', todo=todos[todo_id])
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if 0 <= todo_id < len(todos):
        todos.pop(todo_id)
    return redirect(url_for('index'))

@app.route('/complete/<int:todo_id>', methods=['POST'])
def complete_task(todo_id):
    if 0 <= todo_id < len(todos):
        completed_todos.append(todos.pop(todo_id))
    return redirect(url_for('index'))

@app.route('/restore/<int:todo_id>', methods=['POST'])
def restore_task(todo_id):
    if 0 <= todo_id < len(completed_todos):
        todos.append(completed_todos.pop(todo_id))
    return redirect(url_for('completed_tasks'))

@app.route('/delete_all_completed', methods=['POST'])
def delete_all_completed():
    completed_todos.clear()  # すべての完了済みタスクを削除
    return redirect(url_for('completed_tasks'))

@app.route('/completed')
def completed_tasks():
    return render_template('completed_tasks.html', todos=completed_todos)

if __name__ == '__main__':
    app.run(debug=True)
