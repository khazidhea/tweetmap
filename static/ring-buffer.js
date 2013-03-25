RingBuffer = function(capacity) {
	this.pointer = 0;
  	this.buffer = new Array(capacity); 
  	this.capacity = capacity;
  	this.length = 0;
  	return this;
};

RingBuffer.prototype.push = function(value) {
	if (this.length < this.capacity) {
		++this.length;
	}
	this.buffer[this.pointer++] = value;
	if (this.pointer >= this.capacity) {
		this.pointer = this.pointer % this.capacity;
	}
}

RingBuffer.prototype.get = function(key) {
	return this.buffer[key];
}


RingBuffer.prototype.get_array = function() {
	var result = [];
	for (var i = 0; i < this.length; ++i) {
		result.push(this.buffer[i]);
	}
	return result;
}