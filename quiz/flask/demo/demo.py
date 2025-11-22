from flask import Flask, request, jsonify 
from datetime import datetime 
from typing import Optional 

app = Flask(__name__)

sessions = [] 
next_session_id = 1 
def calculate_duration(started_at, stopped_at):
    duration = (stopped_at-started_at).total_seconds()
    return int(duration)
def search(session_id):
    for s in sessions:
        if s['session_id'] == session_id:
            return s 
    return None 

@app.route('/sessions/start', methods = ['POST'])
def start_session():
    global next_session_id
    data = request.get_json()
    task_name = data.get('task_name', "")
    if len(task_name)<3 or len(task_name)>20:
        return jsonify(
            {
                "error": "Invalid task name",
                "message": "Task name must be between 3 and 20 characters"
            }
        )
    session = {
        "session_id":next_session_id,
        "task_name":task_name,
        "started_at": datetime.now(),
        "stopped_at": None, 
        "duration_seconds":None,
        "status": "running"
    }
    sessions.append(session)
    next_session_id+=1
    return jsonify(
        {
            "session_id":session['session_id'],
            "task_name":session['task_name'], 
            "started_at":session['started_at'].isoformat(),
            "status":session['status']
        }
    ), 201


@app.route('/sessions/<int:session_id>/stop', methods = ['POST'])
def stop_session(session_id):
    stopped_at = datetime.now()
    session = search(session_id)
    if not session:
        return jsonify(
            {
                "error": "Session not found",
                "message": f"No session with ID {session_id}"
            }
        ), 404
    elif session['status'] == 'completed':
        return jsonify(
            {
                "error": "Session already stopped",
                "message": f"Session {session_id} was already stopped"
            }
        ),400
    else:
        session['status']="completed"
        session['stopped_at'] = stopped_at
        session['duration_seconds'] = calculate_duration(session['started_at'], session['stopped_at'])
        return jsonify(
            {
                "session_id": session_id,
                "task_name": session['task_name'],
                "started_at": session['started_at'].isoformat(),
                "stopped_at": session['stopped_at'].isoformat(),
                "duration_seconds": session['duration_seconds'],
                "status": session['status']
            }
        ), 200
    
@app.route('/sessions', methods = ["GET"])
def get_sessions():
    status = request.args.get('status')
    if status:
        res = [s for s in sessions if s['status'] == status]
    else:
        res = sessions
    payload = [] 
    for s in res:
        if s['status'] == 'running':
            stopped_at = datetime.now()
            duration = calculate_duration(s['started_at'], stopped_at)
        else:
            stopped_at = s['stopped_at']
            duration = s['duration_seconds']

        payload.append({
            'session_id': s['session_id'], 
            'task_name': s['task_name'],
            'started_at': s['started_at'].isoformat(),
            'stopped_at': stopped_at.isoformat(),
            'duration_seconds': duration,
            'status': s['status']
        })

    return jsonify(
        {
            'sessions': payload,
            "total": len(res)
        }
    ), 200


@app.route('/sessions/<int:session_id>', methods = ['GET'])
def get_session_by_id(session_id):
    session = search(session_id)
    if not session:
        return jsonify(
            {
                "error": "Session not found",
                "message": f"No session with ID {session_id}"
            }
        ), 404
    else:
        if session['status']=='running':
            stopped_at = datetime.now()
            duration = calculate_duration(session['started_at'], stopped_at)
        else:
            duration = session['duration_seconds']
        return jsonify(
            {
                "session_id": session['session_id'],
                "task_name":session['task_name'],
                'started_at':session['started_at'].isoformat(),
                'stopped_at':stopped_at.isoformat(),
                'duration_seconds':duration,
                'status':session['status']
            }
        ), 200

@app.route('/sessions/<int:session_id>', methods = ['DELETE'])
def delete_session(session_id):
    session = search(session_id)
    if not session:
        return jsonify(
            {
                "error": "Session not found",
                "message": f"No session with ID {session_id}"
            }
        ), 404
    else:
        sessions.remove(session)
        return jsonify(
            {
                "message": "Session deleted successfully",
                "session_id": session_id,
                "task_name": session['task_name']
            }
        ), 200
    
if __name__ == '__main__':
    app.run(debug= True)

    



