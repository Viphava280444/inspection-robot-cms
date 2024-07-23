import React, { useState, useEffect } from "react";
import NavBar from "./components/NavBar";
import HSVControls from "./components/HSVControls";
import VideoStream from "./components/VideoStream";
import ControlPanel from "./components/ControlPanel";
import StatusControl from "./components/StatusControl";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col } from "react-bootstrap";
import "./index.css";
import config from "./config"; // Import the config

function App() {
  const [hsv, setHsv] = useState({
    h_min: 0,
    h_max: 179,
    s_min: 0,
    s_max: 255,
    v_min: 0,
    v_max: 255,
  });

  useEffect(() => {
    // Fetch initial HSV values
    fetch(`${config.baseURL}/hsv`)
      .then((response) => response.json())
      .then((data) => setHsv(data));
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setHsv((prevHsv) => ({
      ...prevHsv,
      [name]: parseInt(value),
    }));

    // Send updated HSV values to the server
    fetch(`${config.baseURL}/hsv`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ [name]: parseInt(value) }),
    });
  };

  return (
    <div className="App">
      <NavBar />
      <Container fluid className="full-height-container pt-2">
        <Row className="full-height-row">
          <Col md={4} className="full-height-col mb-4">
            <VideoStream
              src={`${config.baseURL}/video_normal`}
            />
          </Col>
          <Col md={4} className="full-height-col mb-4">
            <VideoStream
              src={`${config.baseURL}/video_mask`}
            />
          </Col>
          <Col md={4} className="full-height-col mb-4">
            <VideoStream
              title="Combined Video"
              src={`${config.baseURL}/video_combined`}
            />
          </Col>
        </Row>
        <Row className="full-height-row">
          <Col md={4} className="full-height-col mb-4">
            <HSVControls hsv={hsv} handleChange={handleChange} />
          </Col>
          <Col md={4} className="full-height-col mb-4">
            <ControlPanel />
          </Col>
          <Col md={4} className="full-height-col mb-4">
            <StatusControl />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
