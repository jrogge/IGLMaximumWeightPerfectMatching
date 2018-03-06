var heightMap = [0.0 , 0.0243902439024 , 0.0487804878049 , 0.0731707317073 , 0.0975609756098 , 0.121951219512 , 0.146341463415 , 0.170731707317 , 0.19512195122 , 0.219512195122 , 0.243902439024 , 0.268292682927 , 0.292682926829 , 0.317073170732 , 0.341463414634 , 0.365853658537 , 0.390243902439 , 0.414634146341 , 0.439024390244 , 0.463414634146 , 0.487804878049 , 0.512195121951 , 0.536585365854 , 0.560975609756 , 0.585365853659 , 0.609756097561 , 0.634146341463 , 0.658536585366 , 0.682926829268 , 0.707317073171 , 0.731707317073 , 0.756097560976 , 0.780487804878 , 0.80487804878 , 0.829268292683 , 0.853658536585 , 0.878048780488 , 0.90243902439 , 0.926829268293 , 0.951219512195 , 0.975609756098];

/**
 * @fileoverview Terrain - A simple 3D terrain using WebGL
 * @author Eric Shaffer
 */

/** Class implementing 3D terrain. */
class Terrain{   
/**
 * Initialize members of a Terrain object
 * @param {number} div Number of triangles along x axis and y axis
 * @param {number} minX Minimum X coordinate value
 * @param {number} maxX Maximum X coordinate value
 * @param {number} minY Minimum Y coordinate value
 * @param {number} maxY Maximum Y coordinate value
 */
    constructor(div,minX,maxX,minY,maxY){
        this.div = div;
        this.minX=minX;
        this.minY=minY;
        this.maxX=maxX;
        this.maxY=maxY;
        
        // Allocate vertex array
        this.vBuffer = [];
        // Allocate triangle array
        this.fBuffer = [];
        // Allocate normal array
        this.nBuffer = [];
        // Allocate array for edges so we can draw wireframe
        this.eBuffer = [];
        console.log("Terrain: Allocated buffers");
        
        this.generateTriangles();
        console.log("Terrain: Generated triangles");

        this.populateHeights();
        
        this.generateLines();
        console.log("Terrain: Generated lines");
        
        // Get extension for 4 byte integer indices for drwElements
        var ext = gl.getExtension('OES_element_index_uint');
        if (ext ==null){
            alert("OES_element_index_uint is unsupported by your browser and terrain generation cannot proceed.");
        }
    }
    
    /**
    * Set the x,y,z coords of a vertex at location(i,j)
    * @param {Object} v an an array of length 3 holding x,y,z coordinates
    * @param {number} i the ith row of vertices
    * @param {number} j the jth column of vertices
    */
    setVertex(v,i,j)
    {
        var vid = 3 * (i * (this.div + 1) + j);
        this.vBuffer[vid] = v[0];
        this.vBuffer[vid + 1] = v[1];
        this.vBuffer[vid + 2] = v[2];
    }
    
    /**
    * Return the x,y,z coordinates of a vertex at location (i,j)
    * @param {Object} v an an array of length 3 holding x,y,z coordinates
    * @param {number} i the ith row of vertices
    * @param {number} j the jth column of vertices
    */
    getVertex(v,i,j)
    {
        var vid = 3 * (i * (this.div + 1) + j);
        v.push(this.vBuffer[vid]);
        v.push(this.vBuffer[vid+1]);
        v.push(this.vBuffer[vid+2]);
    }
    
    /**
    * Send the buffer objects to WebGL for rendering 
    */
    loadBuffers()
    {
        // Specify the vertex coordinates
        this.VertexPositionBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.VertexPositionBuffer);      
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.vBuffer), gl.STATIC_DRAW);
        this.VertexPositionBuffer.itemSize = 3;
        this.VertexPositionBuffer.numItems = this.numVertices;
        console.log("Loaded ", this.VertexPositionBuffer.numItems, " vertices");
    
        // Specify normals to be able to do lighting calculations
        this.VertexNormalBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, this.VertexNormalBuffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.nBuffer),
                  gl.STATIC_DRAW);
        this.VertexNormalBuffer.itemSize = 3;
        this.VertexNormalBuffer.numItems = this.numVertices;
        console.log("Loaded ", this.VertexNormalBuffer.numItems, " normals");
    
        // Specify faces of the terrain 
        this.IndexTriBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.IndexTriBuffer);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(this.fBuffer),
                  gl.STATIC_DRAW);
        this.IndexTriBuffer.itemSize = 1;
        this.IndexTriBuffer.numItems = this.fBuffer.length;
        console.log("Loaded ", this.IndexTriBuffer.numItems, " triangles");
    
        //Setup Edges  
        this.IndexEdgeBuffer = gl.createBuffer();
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.IndexEdgeBuffer);
        gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(this.eBuffer),
                  gl.STATIC_DRAW);
        this.IndexEdgeBuffer.itemSize = 1;
        this.IndexEdgeBuffer.numItems = this.eBuffer.length;
        
        console.log("triangulatedPlane: loadBuffers");
    }
    
    /**
    * Render the triangles 
    */
    drawTriangles(){
        gl.bindBuffer(gl.ARRAY_BUFFER, this.VertexPositionBuffer);
        gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, this.VertexPositionBuffer.itemSize, 
                         gl.FLOAT, false, 0, 0);

        // Bind normal buffer
        gl.bindBuffer(gl.ARRAY_BUFFER, this.VertexNormalBuffer);
        gl.vertexAttribPointer(shaderProgram.vertexNormalAttribute, 
                           this.VertexNormalBuffer.itemSize,
                           gl.FLOAT, false, 0, 0);   
    
        //Draw 
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.IndexTriBuffer);
        gl.drawElements(gl.TRIANGLES, this.IndexTriBuffer.numItems, gl.UNSIGNED_INT,0);
    }
    
    /**
    * Render the triangle edges wireframe style 
    */
    drawEdges(){
    
        gl.bindBuffer(gl.ARRAY_BUFFER, this.VertexPositionBuffer);
        gl.vertexAttribPointer(shaderProgram.vertexPositionAttribute, this.VertexPositionBuffer.itemSize, 
                         gl.FLOAT, false, 0, 0);

        // Bind normal buffer
        gl.bindBuffer(gl.ARRAY_BUFFER, this.VertexNormalBuffer);
        gl.vertexAttribPointer(shaderProgram.vertexNormalAttribute, 
                           this.VertexNormalBuffer.itemSize,
                           gl.FLOAT, false, 0, 0);   
    
        //Draw 
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.IndexEdgeBuffer);
        gl.drawElements(gl.LINES, this.IndexEdgeBuffer.numItems, gl.UNSIGNED_INT,0);   
    }
/**
 * Fill the vertex and buffer arrays 
 */    
generateTriangles()
{
    var deltaX = (this.maxX - this.minX) / this.div;
    var deltaY = (this.maxY - this.minY) / this.div;
    for (var j = 0; j <= this.div; j++) {
        for (var i = 0; i <= this.div; i++) {
            // vertex
            this.vBuffer.push(this.minX + deltaX * i);
            this.vBuffer.push(this.minY + deltaY * j);
            this.vBuffer.push(0);
            //this.vBuffer.push(j / this.div);
            //var curr_index = j * (this.div+1) + i;
            //this.vBuffer.push(heightMap[curr_index]);
            //console.log(heightMap[curr_index]);

            // normals
            this.nBuffer.push(0);
            this.nBuffer.push(0);
            this.nBuffer.push(1);
        }
    }

    for (var i = 0; i < this.div; i++) {
        for (var j = 0; j < this.div; j++) {
            var vid = i*(this.div+1) + j;
            this.fBuffer.push(vid);
            this.fBuffer.push(vid+1);
            this.fBuffer.push(vid+this.div+1);

            this.fBuffer.push(vid+1);
            this.fBuffer.push(vid+1+this.div+1);
            this.fBuffer.push(vid+this.div+1);
        }
    }
    //
    this.numVertices = this.vBuffer.length/3;
    this.numFaces = this.fBuffer.length/3;
}

/**
 * Print vertices and triangles to console for debugging
 */
printBuffers()
    {
        
    for(var i=0;i<this.numVertices;i++)
          {
           console.log("v ", this.vBuffer[i*3], " ", 
                             this.vBuffer[i*3 + 1], " ",
                             this.vBuffer[i*3 + 2], " ");
                       
          }
    
      for(var i=0;i<this.numFaces;i++)
          {
           console.log("f ", this.fBuffer[i*3], " ", 
                             this.fBuffer[i*3 + 1], " ",
                             this.fBuffer[i*3 + 2], " ");
                       
          }
        
    }

/**
 * Generates line values from faces in faceArray
 * to enable wireframe rendering
 */
generateLines()
{
    var numTris=this.fBuffer.length/3;
    for(var f=0;f<numTris;f++)
    {
        var fid=f*3;
        this.eBuffer.push(this.fBuffer[fid]);
        this.eBuffer.push(this.fBuffer[fid+1]);
        
        this.eBuffer.push(this.fBuffer[fid+1]);
        this.eBuffer.push(this.fBuffer[fid+2]);
        
        this.eBuffer.push(this.fBuffer[fid+2]);
        this.eBuffer.push(this.fBuffer[fid]);
    }
    
}

/**
 * use heightMap generated by python proram to make visualization
 */
populateHeights()
{
    var counter = 0;
    var midVal = this.div / 2.0
    // 0 is an odd edge case, handle manually
    var midHeight = heightMap[0] / (2 * this.div);
    this.setVertex([0, 0, midHeight], midVal, midVal);
    console.log("mid val: ", midVal);
    counter++;
    var halfDiv = this.div / 2.0;
    for (var i = 1; i <= halfDiv; i++) {
        console.log("i: ", i);
        var curr = [];
        var x = -42;
        // TODO: do this better
        for (var y = 0; y < i; y++) {
            x = i - y;
            var xTrans = x + halfDiv; // hacky way to properly align
            var yTrans = y + halfDiv; // hacky way to properly align
            this.getVertex(curr, yTrans, xTrans);
            var newHeight = heightMap[counter] / (2 * this.div);
            this.setVertex([curr[0], curr[1], newHeight], yTrans,
                    xTrans);
            console.log(heightMap[counter]);
            curr = []; // getVertex pushes to array, need to flush it each time
            counter++;
        }
        for (var y = i; y > 0; y--) {
            x = y - i;
            var xTrans = x + halfDiv; // hacky way to properly align
            var yTrans = y + halfDiv; // hacky way to properly align
            this.getVertex(curr, yTrans, xTrans);
            var newHeight = heightMap[counter] / (2 * this.div);
            this.setVertex([curr[0], curr[1], newHeight], yTrans,
                    xTrans);
            console.log(heightMap[counter]);
            curr = [];
            counter++;
        }
        // TODO: do this better
        //var xTrans = x + halfDiv; // hacky way to properly align
        for (var y = 0; y > -1 * i; y--) {
            x = Math.abs(y) - i;
            var xTrans = x + halfDiv; // hacky way to properly align
            var yTrans = y + halfDiv; // hacky way to properly align
            this.getVertex(curr, yTrans, xTrans);
            var newHeight = heightMap[counter] / (2 * this.div);
            this.setVertex([curr[0], curr[1], newHeight], yTrans,
                    xTrans);
            console.log(heightMap[counter]);
            curr = [];
            counter++;
        }
        for (var y = -1 * i; y < 0; y++) {
            x = y + i;
            var xTrans = x + halfDiv; // hacky way to properly align
            var yTrans = y + halfDiv; // hacky way to properly align
            this.getVertex(curr, yTrans, xTrans);
            var newHeight = heightMap[counter] / (2 * this.div);
            this.setVertex([curr[0], curr[1], newHeight], yTrans,
                    xTrans);
            console.log(heightMap[counter]);
            curr = [];
            counter++;
        }
    }
}
    
}
