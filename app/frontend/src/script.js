document.getElementById('uploadForm').addEventListener('submit', async function (e) {
    e.preventDefault();
  
    const form = e.target;
    const formData = new FormData(form);
  
    const responseContainer = document.getElementById('agentResponses');
    responseContainer.innerHTML = 'Processing...';
  
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        body: formData,
      });
  
      if (!res.ok) {
        throw new Error("Failed to submit");
      }
  
      const reader = res.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let chunkText = "";
  
      responseContainer.innerHTML = "";
  
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
  
        chunkText += decoder.decode(value, { stream: true });
  
        const chunks = chunkText.split("\n").filter(Boolean);
        chunkText = "";
  
        chunks.forEach(chunk => {
          try {
            const data = JSON.parse(chunk);
  
            if (data.type === "agent") {
              const agentDiv = document.createElement('div');
              agentDiv.className = "agent-block";
              agentDiv.dataset.sessionId = data.session_id;

  
              agentDiv.innerHTML = `
                <div><strong>${data.agent_name}</strong></div>
                <textarea>${JSON.stringify(data.contract, null, 2)}</textarea>
                <div class="button-wrapper">
                  <button class="submit-agent" onclick="submitAgent('${data.agent_name}', this)">Submit</button>
                </div>
              `;
  
              responseContainer.appendChild(agentDiv);
            } else if (data.type === "final") {
              createDownloadBlock(data.final_contract);
            }
          } catch (err) {
            console.error("Stream parsing error:", err, chunk);
          }
        });
      }
  
    } catch (err) {
      alert("Something went wrong: " + err.message);
    }
  });
  
  function submitAgent(agentName, btn) {
    const agentDiv = btn.closest('.agent-block');
    const textarea = agentDiv.querySelector('textarea');
    const sessionId = agentDiv.dataset.sessionId;
  
    let updatedContract;
  
    try {
      updatedContract = JSON.parse(textarea.value);
    } catch (err) {
      alert("Invalid JSON format. Please fix it before submitting.");
      return;
    }
  
    btn.disabled = true;
    btn.textContent = "Submitting...";
  
    fetch("/api/update-agent-contract", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        agent_name: agentName,
        contract: updatedContract,
        session_id: sessionId
      })
    })
      .then(res => {
        if (!res.ok) throw new Error("Submission failed");
        return res.json();
      })
      .then((data) => {
        if (data.type === "agent") {
          // Continue to next agent
          const responseContainer = document.getElementById('agentResponses');
  
          const newAgentDiv = document.createElement('div');
          newAgentDiv.className = "agent-block";
          newAgentDiv.dataset.sessionId = data.session_id;
  
          newAgentDiv.innerHTML = `
            <div><strong>${data.agent_name}</strong></div>
            <textarea>${JSON.stringify(data.contract, null, 2)}</textarea>
            <div class="button-wrapper">
              <button class="submit-agent" onclick="submitAgent('${data.agent_name}', this)">Submit</button>
            </div>
          `;
  
          responseContainer.appendChild(newAgentDiv);
        } else if (data.type === "final") {
          createDownloadBlock(data.final_contract);
        }
  
        btn.remove(); // hide the old submit button
      })
      .catch(err => {
        console.error(err);
        btn.textContent = "Submit";
        btn.disabled = false;
        alert("Failed to submit. See console for details.");
      });
  }
  