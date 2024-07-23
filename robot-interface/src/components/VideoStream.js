import React from "react";
import { Card } from "react-bootstrap";

const VideoStream = ({ title, src }) => {
  return (
    <Card className="stream-card">
      <Card.Body>
        <Card.Title>{title}</Card.Title>
        <img src={src} alt={title} className="w-100 h-100" />
      </Card.Body>
    </Card>
  );
};

export default VideoStream;
