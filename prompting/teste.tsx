import React, { useState } from 'react';

// Final A1 with removed internal borders
const FinalA1 = () => (
  <div className="w-full" style={{
    backgroundColor: "#F9F7F4",
    color: "#000",
    fontFamily: "'Bebas Neue', Helvetica, Arial, sans-serif"
  }}>
    {/* Header - REMOVED INTERNAL BORDERS */}
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "30px 0",
      position: "relative",
      borderBottom: "2px solid #9D0208",
      background: "#F9F7F4"
    }}>
      <div style={{
        position: "relative",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "0 20px"
      }}>
        <div style={{
          fontSize: "16px",
          letterSpacing: "5px",
          color: "#D00000",
          marginBottom: "5px",
          textAlign: "center"
          // Removed border
        }}>
          LEGAL AI ENGINEERING
        </div>

        <h1 style={{
          fontSize: "64px",
          fontWeight: "bold",
          margin: 0,
          textAlign: "center",
          letterSpacing: "2px",
          textTransform: "uppercase",
          lineHeight: "1",
          color: "#000",
          padding: "10px"
          // Removed border
        }}>
          PROMPTING<br/>TECHNIQUES
        </h1>

        <div style={{
          fontSize: "20px",
          marginTop: "15px",
          color: "#333",
          textAlign: "center"
          // Removed border
        }}>
          MASTER THE ART OF COMMANDING AI LANGUAGE MODELS
        </div>

        <div style={{
          width: "50px",
          height: "5px",
          background: "#9D0208",
          margin: "20px 0"
        }}></div>

        <div style={{
          display: "flex",
          alignItems: "center"
          // Removed border
        }}>
          <div style={{
            width: "30px",
            height: "2px",
            background: "#E5383B"
          }}></div>
          <div style={{
            padding: "0 10px",
            fontSize: "16px",
            color: "#333"
          }}>BY ARTHUR SOUZA RODRIGUES</div>
          <div style={{
            width: "30px",
            height: "2px",
            background: "#E5383B"
          }}></div>
        </div>
      </div>
    </div>

    {/* Welcome Section - REMOVED INTERNAL BORDERS */}
    <div style={{
      padding: "40px 30px",
      background: "#fff"
    }}>
      <div style={{
        display: "flex",
        alignItems: "flex-start",
        gap: "30px"
      }}>
        <div style={{
          flex: "1",
          borderLeft: "3px solid #D00000",
          paddingLeft: "20px"
        }}>
          <h2 style={{
            fontSize: "36px",
            fontWeight: "bold",
            margin: "0 0 20px 0",
            textTransform: "uppercase",
            letterSpacing: "1px",
            color: "#000"
          }}>WELCOME TO<br/>THE REVOLUTION</h2>

          <p style={{
            fontFamily: "'Inter', sans-serif",
            fontSize: "16px",
            lineHeight: "1.6",
            marginBottom: "20px",
            color: "#333"
            // Removed border
          }}>
            This interactive guide will transform how you interact with AI language models, specifically optimized for legal applications. Each technique is battle-tested in real-world legal scenarios.
          </p>

          <p style={{
            fontFamily: "'Inter', sans-serif",
            fontSize: "16px",
            lineHeight: "1.6",
            marginBottom: "20px",
            color: "#333"
            // Removed border
          }}>
            Through this course, you'll learn how to extract precise, actionable legal analysis instead of generic responses that waste your valuable time.
          </p>
        </div>

        <div style={{
          flex: "1",
          borderRight: "3px solid #D00000",
          paddingRight: "20px"
        }}>
          <div style={{
            background: "#F5CAC3",
            padding: "25px",
            marginBottom: "20px"
          }}>
            <h3 style={{
              fontSize: "24px",
              margin: "0 0 15px 0",
              color: "#9D0208",
              textTransform: "uppercase",
              letterSpacing: "1px"
            }}>COURSE MODULES</h3>

            <ol style={{
              padding: "0 0 0 20px",
              margin: "0",
              fontFamily: "'Inter', sans-serif",
              color: "#333"
            }}>
              <li style={{ marginBottom: "10px" }}>
                <span style={{ color: "#000", fontWeight: "bold" }}>ROLE-BASED PROMPTS</span> - Command authority
              </li>
              <li style={{ marginBottom: "10px" }}>
                <span style={{ color: "#000", fontWeight: "bold" }}>CONTEXT-RICH INSTRUCTIONS</span> - Leave nothing to chance
              </li>
              <li style={{ marginBottom: "10px" }}>
                <span style={{ color: "#000", fontWeight: "bold" }}>CONSTRAINT-BASED COMMANDS</span> - Limit the AI's scope
              </li>
              <li style={{ marginBottom: "10px" }}>
                <span style={{ color: "#000", fontWeight: "bold" }}>STEP-BY-STEP ANALYSIS</span> - Force methodical reasoning
              </li>
              <li style={{ marginBottom: "10px" }}>
                <span style={{ color: "#000", fontWeight: "bold" }}>CONTRACT EXTRACTION</span> - Surgical precision
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>

    {/* Interactive Element */}
    <div style={{
      padding: "40px 30px",
      background: "#000000",
      color: "#FFFFFF",
      border: "2px solid #9D0208",
    }}>
      <h3 style={{
        fontSize: "28px",
        fontWeight: "bold",
        margin: "0 0 30px 0",
        textTransform: "uppercase",
        letterSpacing: "1px",
        textAlign: "center",
        borderBottom: "1px solid #9D0208",
        paddingBottom: "10px",
      }}>TECHNIQUE SELECTOR</h3>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "15px",
        marginBottom: "30px"
      }}>
        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 10px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          CONTRACTS
        </button>

        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 10px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          LITIGATION
        </button>

        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 10px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          CORPORATE
        </button>
      </div>

      <div style={{
        background: "#F5F5F5",
        padding: "25px",
        marginBottom: "30px",
        border: "1px solid #9D0208",
        color: "#000000"
      }}>
        <div style={{
          fontSize: "16px",
          marginBottom: "15px",
          color: "#000000",
          fontFamily: "'Inter', sans-serif",
          fontWeight: "bold"
        }}>SELECTED PROMPT:</div>

        <div style={{
          fontFamily: "'Inter', sans-serif",
          padding: "15px",
          background: "#FFFFFF",
          color: "#000000",
          fontSize: "14px",
          lineHeight: "1.5",
          overflowX: "auto",
          border: "1px solid #9D0208",
        }}>
          AS A CONTRACT LAW SPECIALIST, REVIEW THIS MASTER SERVICE AGREEMENT FOR {`{specific_issue}`} AND IDENTIFY POTENTIAL RISKS RELATED TO {`{risk_area}`}. FOCUS ON CLAUSES THAT MIGHT {`{specific_concern}`}.
        </div>
      </div>

      <div style={{
        textAlign: "center"
      }}>
        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 40px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          EXECUTE
        </button>
      </div>
    </div>
  </div>
);

// Final B2 with removed internal borders
const FinalB2 = () => (
  <div className="w-full" style={{
    backgroundColor: "#FFFFFF",
    color: "#000000",
    fontFamily: "'Bebas Neue', Helvetica, Arial, sans-serif",
    border: "2px solid #9D0208"
  }}>
    {/* Header - REMOVED INTERNAL BORDERS */}
    <div style={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "30px 0",
      position: "relative",
      borderBottom: "4px solid #9D0208",
      background: "#F9F7F4"
    }}>
      <div style={{
        position: "relative",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "0 20px"
      }}>
        <div style={{
          fontSize: "16px",
          letterSpacing: "5px",
          color: "#9D0208",
          marginBottom: "5px",
          textAlign: "center",
          padding: "5px 10px"
          // Removed border
        }}>
          LEGAL AI ENGINEERING
        </div>

        <h1 style={{
          fontSize: "64px",
          fontWeight: "bold",
          margin: "10px 0",
          textAlign: "center",
          letterSpacing: "2px",
          textTransform: "uppercase",
          lineHeight: "1",
          color: "#000000",
          padding: "10px"
          // Removed border
        }}>
          PROMPTING<br/>TECHNIQUES
        </h1>

        <div style={{
          fontSize: "20px",
          marginTop: "15px",
          color: "#333",
          textAlign: "center",
          padding: "5px 15px"
          // Removed border
        }}>
          MASTER THE ART OF COMMANDING AI LANGUAGE MODELS
        </div>

        <div style={{
          width: "50px",
          height: "5px",
          background: "#9D0208",
          margin: "20px 0"
          // Removed border
        }}></div>

        <div style={{
          display: "flex",
          alignItems: "center",
          padding: "5px 10px"
          // Removed border
        }}>
          <div style={{
            width: "30px",
            height: "2px",
            background: "#9D0208"
          }}></div>
          <div style={{
            padding: "0 10px",
            fontSize: "16px",
            color: "#333"
          }}>BY ARTHUR SOUZA RODRIGUES</div>
          <div style={{
            width: "30px",
            height: "2px",
            background: "#9D0208"
          }}></div>
        </div>
      </div>
    </div>

    {/* Welcome Section - REMOVED INTERNAL BORDERS */}
    <div style={{
      padding: "40px 30px",
      background: "#FFFFFF",
      border: "1px solid #9D0208",
      margin: "10px",
    }}>
      <div style={{
        display: "flex",
        alignItems: "flex-start",
        gap: "30px"
      }}>
        <div style={{
          flex: "1",
          borderLeft: "5px solid #9D0208",
          paddingLeft: "20px",
          padding: "20px"
          // Removed border
        }}>
          <h2 style={{
            fontSize: "36px",
            fontWeight: "bold",
            margin: "0 0 20px 0",
            textTransform: "uppercase",
            letterSpacing: "1px",
            color: "#000000",
            borderBottom: "2px solid #9D0208",
            paddingBottom: "10px",
          }}>WELCOME TO<br/>THE REVOLUTION</h2>

          <p style={{
            fontFamily: "'Inter', sans-serif",
            fontSize: "16px",
            lineHeight: "1.6",
            marginBottom: "20px",
            color: "#333",
            padding: "10px"
            // Removed border
          }}>
            This interactive guide will transform how you interact with AI language models, specifically optimized for legal applications. Each technique is battle-tested in real-world legal scenarios.
          </p>

          <p style={{
            fontFamily: "'Inter', sans-serif",
            fontSize: "16px",
            lineHeight: "1.6",
            marginBottom: "20px",
            color: "#333",
            padding: "10px"
            // Removed border
          }}>
            Through this course, you'll learn how to extract precise, actionable legal analysis instead of generic responses that waste your valuable time.
          </p>
        </div>

        <div style={{
          flex: "1",
          borderRight: "5px solid #9D0208",
          paddingRight: "20px"
        }}>
          <div style={{
            background: "#F5F5F5",
            padding: "25px",
            marginBottom: "20px",
            border: "2px solid #9D0208",
          }}>
            <h3 style={{
              fontSize: "24px",
              margin: "0 0 15px 0",
              color: "#9D0208",
              textTransform: "uppercase",
              letterSpacing: "1px",
              borderBottom: "2px solid #9D0208",
              paddingBottom: "5px",
            }}>COURSE MODULES</h3>

            <ol style={{
              padding: "0 0 0 20px",
              margin: "0",
              fontFamily: "'Inter', sans-serif",
              color: "#333"
            }}>
              <li style={{ marginBottom: "10px", borderBottom: "1px solid #9D0208", paddingBottom: "5px" }}>
                <span style={{ color: "#000000", fontWeight: "bold" }}>ROLE-BASED PROMPTS</span> - Command authority
              </li>
              <li style={{ marginBottom: "10px", borderBottom: "1px solid #9D0208", paddingBottom: "5px" }}>
                <span style={{ color: "#000000", fontWeight: "bold" }}>CONTEXT-RICH INSTRUCTIONS</span> - Leave nothing to chance
              </li>
              <li style={{ marginBottom: "10px", borderBottom: "1px solid #9D0208", paddingBottom: "5px" }}>
                <span style={{ color: "#000000", fontWeight: "bold" }}>CONSTRAINT-BASED COMMANDS</span> - Limit the AI's scope
              </li>
              <li style={{ marginBottom: "10px", borderBottom: "1px solid #9D0208", paddingBottom: "5px" }}>
                <span style={{ color: "#000000", fontWeight: "bold" }}>STEP-BY-STEP ANALYSIS</span> - Force methodical reasoning
              </li>
              <li style={{ marginBottom: "10px", borderBottom: "1px solid #9D0208", paddingBottom: "5px" }}>
                <span style={{ color: "#000000", fontWeight: "bold" }}>CONTRACT EXTRACTION</span> - Surgical precision
              </li>
            </ol>
          </div>
        </div>
      </div>
    </div>

    {/* Interactive Element */}
    <div style={{
      padding: "40px 30px",
      background: "#000000",
      color: "#FFFFFF",
      border: "4px solid #9D0208",
      margin: "10px",
    }}>
      <h3 style={{
        fontSize: "28px",
        fontWeight: "bold",
        margin: "0 0 30px 0",
        textTransform: "uppercase",
        letterSpacing: "1px",
        textAlign: "center",
        borderBottom: "2px solid #9D0208",
        paddingBottom: "10px",
      }}>TECHNIQUE SELECTOR</h3>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(3, 1fr)",
        gap: "15px",
        marginBottom: "30px"
      }}>
        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 10px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          CONTRACTS
        </button>

        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 10px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          LITIGATION
        </button>

        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 10px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          CORPORATE
        </button>
      </div>

      <div style={{
        background: "#F5F5F5",
        padding: "25px",
        marginBottom: "30px",
        border: "2px solid #9D0208",
        color: "#000000"
      }}>
        <div style={{
          fontSize: "16px",
          marginBottom: "15px",
          color: "#000000",
          fontFamily: "'Inter', sans-serif",
          fontWeight: "bold",
          borderBottom: "1px solid #9D0208",
          paddingBottom: "5px",
        }}>SELECTED PROMPT:</div>

        <div style={{
          fontFamily: "'Inter', sans-serif",
          padding: "15px",
          background: "#FFFFFF",
          color: "#000000",
          fontSize: "14px",
          lineHeight: "1.5",
          overflowX: "auto",
          border: "1px solid #9D0208",
        }}>
          AS A CONTRACT LAW SPECIALIST, REVIEW THIS MASTER SERVICE AGREEMENT FOR {`{specific_issue}`} AND IDENTIFY POTENTIAL RISKS RELATED TO {`{risk_area}`}. FOCUS ON CLAUSES THAT MIGHT {`{specific_concern}`}.
        </div>
      </div>

      <div style={{
        textAlign: "center"
      }}>
        <button style={{
          background: "#E5383B",
          color: "#FFFFFF",
          border: "2px solid #9D0208",
          padding: "15px 40px",
          fontSize: "18px",
          fontWeight: "bold",
          cursor: "pointer",
          textTransform: "uppercase",
          letterSpacing: "2px"
        }}>
          EXECUTE
        </button>
      </div>
    </div>
  </div>
);

const App = () => {
  const [activeDesign, setActiveDesign] = useState(1);

  return (
    <div className="p-4">
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Final Designs</h2>

        <div className="mb-6">
          <p className="text-sm text-gray-600 mb-2">
            <strong>Final improvements:</strong>
          </p>
          <ul className="text-sm text-gray-600 list-disc pl-5 mb-4">
            <li>Removed internal borders from header elements while maintaining overall structure</li>
            <li>Removed borders from text paragraphs in the welcome section for cleaner readability</li>
            <li>Preserved padding to maintain spacing and visual hierarchy</li>
            <li>Maintained standardized button styles throughout</li>
          </ul>
        </div>

        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => setActiveDesign(1)}
            className={`px-4 py-2 rounded text-sm ${
              activeDesign === 1
                ? 'bg-red-800 text-white'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-800'
            }`}
          >
            Final A1
          </button>
          <button
            onClick={() => setActiveDesign(2)}
            className={`px-4 py-2 rounded text-sm ${
              activeDesign === 2
                ? 'bg-red-800 text-white'
                : 'bg-gray-100 hover:bg-gray-200 text-gray-800'
            }`}
          >
            Final B2
          </button>
        </div>
      </div>

      <div className="border border-gray-200 rounded-lg overflow-hidden bg-white p-4">
        {activeDesign === 1 && <FinalA1 />}
        {activeDesign === 2 && <FinalB2 />}
      </div>
    </div>
  );
};

export default App;
