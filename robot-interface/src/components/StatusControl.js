import React from "react";
import { Card, Button } from "react-bootstrap";

const StatusControl = () => {
  return (
    <Card className="control-card">
      <Card.Body>
        <Card.Title>Status and Control</Card.Title>
        <Card.Text>Status: Active/Inactive</Card.Text>
        <Button variant="success" className="me-2">
          Turn On
        </Button>
        <Button variant="danger">Turn Off</Button>
      </Card.Body>
    </Card>
  );
};

export default StatusControl;
