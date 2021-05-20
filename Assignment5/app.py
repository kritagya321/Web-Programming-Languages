
from flask import Flask, request, json
from bson.objectid import ObjectId
import pymongo

# Create
# Read
# Update 
# Delete

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["vidzy"]
mycol = mydb["videos"]


# Read - list all videos
@app.route("/videos")
def main(): 
    response = []
    for record in mycol.find():
        record['_id'] = str(record['_id'])
        response.append(record)
    return json.dumps(response)



# Read - list an individual video
@app.route('/videos/<id>')
def showVideo(id):

	# return json.dumps({'video id': videoid })
	record = mycol.find_one({'_id' : ObjectId(id) })
	record['_id'] = str(record['_id'])
	return json.dumps(record)


# Create - add a new video
@app.route("/videos", methods=['POST'])
def newVideo():

	title = request.args.get('title')
	desc  = request.args.get('desc')

	new = { "title": title, "description": desc }

	_id = mycol.insert_one(new)
	#return json.dumps({'ObjectId for new movie':str(_id)})
	return json.dumps({'message': 'Video created successfully !'})



# Update - update an existing video
@app.route('/videos/<id>', methods=['PUT'])
def updateVideo(id):

	title = request.args.get('title')
	desc  = request.args.get('desc')

	query = { '_id':  ObjectId(id) }
	newvalues = { "$set": { 'title': title, "description": desc  } }

	mycol.update_one(query, newvalues)

	return json.dumps({'message': 'Video updated successfully !'})

# Delete - delete a video
@app.route('/videos/<id>', methods=['DELETE'])
def deleteVideo(id):

	query = { '_id':  ObjectId(id) }
	mycol.delete_one(query)

	return json.dumps({'message': 'Video deleted successfully !'})




if __name__ == "__main__":
    app.run()   


