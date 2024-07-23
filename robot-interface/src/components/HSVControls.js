import React from "react";
import { Form, Row, Col, Card } from "react-bootstrap";

const HSVControls = ({ hsv, handleChange }) => {
  return (
    <Card className="control-card">
      <Card.Body>
        <Card.Title>HSV Controls</Card.Title>
        <Form>
          <Form.Group as={Row} className="mb-3">
            <Form.Label column sm="2">
              H_MAX
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="range"
                name="h_max"
                min="0"
                max="179"
                value={hsv.h_max}
                onChange={handleChange}
              />
            </Col>
            <Col sm="2">
              <Form.Control type="text" readOnly value={hsv.h_max} />
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3">
            <Form.Label column sm="2">
              H_MIN
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="range"
                name="h_min"
                min="0"
                max="179"
                value={hsv.h_min}
                onChange={handleChange}
              />
            </Col>
            <Col sm="2">
              <Form.Control type="text" readOnly value={hsv.h_min} />
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3">
            <Form.Label column sm="2">
              S_MAX
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="range"
                name="s_max"
                min="0"
                max="255"
                value={hsv.s_max}
                onChange={handleChange}
              />
            </Col>
            <Col sm="2">
              <Form.Control type="text" readOnly value={hsv.s_max} />
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3">
            <Form.Label column sm="2">
              S_MIN
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="range"
                name="s_min"
                min="0"
                max="255"
                value={hsv.s_min}
                onChange={handleChange}
              />
            </Col>
            <Col sm="2">
              <Form.Control type="text" readOnly value={hsv.s_min} />
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3">
            <Form.Label column sm="2">
              V_MAX
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="range"
                name="v_max"
                min="0"
                max="255"
                value={hsv.v_max}
                onChange={handleChange}
              />
            </Col>
            <Col sm="2">
              <Form.Control type="text" readOnly value={hsv.v_max} />
            </Col>
          </Form.Group>
          <Form.Group as={Row} className="mb-3">
            <Form.Label column sm="2">
              V_MIN
            </Form.Label>
            <Col sm="8">
              <Form.Control
                type="range"
                name="v_min"
                min="0"
                max="255"
                value={hsv.v_min}
                onChange={handleChange}
              />
            </Col>
            <Col sm="2">
              <Form.Control type="text" readOnly value={hsv.v_min} />
            </Col>
          </Form.Group>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default HSVControls;
