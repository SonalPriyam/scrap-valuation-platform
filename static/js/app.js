document.addEventListener("DOMContentLoaded", () => {
    const fileInput = document.getElementById("imageFile");
    const fileFeedback = document.getElementById("fileFeedback");
    const dropzone = document.getElementById("dropzone");

    const valuationForm = document.getElementById("valuationForm");
    const submitBtn = document.getElementById("submitBtn");
    const loadingState = document.getElementById("loadingState");
    const resultCard = document.getElementById("resultCard");

    const resMaterial = document.getElementById("resMaterial");
    const resWeight = document.getElementById("resWeight");
    const resQuality = document.getElementById("resQuality");
    const resPrice = document.getElementById("resPrice");
    const resRange = document.getElementById("resRange");

    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            const fileName = e.target.files[0].name;
            const fileSize = (e.target.files[0].size / (1024 * 1024)).toFixed(2);

            fileFeedback.innerText = `Ready: ${fileName} (${fileSize} MB)`;
            fileFeedback.classList.remove("hidden");
            dropzone.classList.add("border-emerald-500", "bg-slate-900/40");
        }
    });

    valuationForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        if (fileInput.files.length === 0) {
            alert("Please drop or select a scrap image before executing valuation.");
            return;
        }

        valuationForm.classList.add("hidden");
        loadingState.classList.remove("hidden");
        resultCard.classList.add("hidden");

        const payload = new FormData();
        payload.append(
            "text_description",
            document.getElementById("textDescription").value
        );
        payload.append("image_file", fileInput.files[0]);

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/api/v1/valuate",
                {
                    method: "POST",
                    body: payload
                }
            );

            if (!response.ok) {
                throw new Error(
                    `Server Pipeline Breakdown. Status Code: ${response.status}`
                );
            }

            const data = await response.json();

            if (data.status === "success") {
                resMaterial.innerText =
                    data.extracted_data.classified_material;

                resWeight.innerText =
                    data.extracted_data.parsed_weight;

                resQuality.innerText =
                    data.extracted_data.condition_grade;

                resPrice.innerText =
                    data.valuation_output.midpoint_estimation;

                resRange.innerText =
                    `Confidence Boundary Range Scale: ${data.valuation_output.market_price_range}`;

                loadingState.classList.add("hidden");
                resultCard.classList.remove("hidden");
                resultCard.classList.add("animate-fade-in");
                valuationForm.classList.remove("hidden");
            } else {
                throw new Error(
                    "Valuation calculation returned an invalid status flag."
                );
            }
        } catch (error) {
            console.error("Pipeline Error:", error);

            alert(`Execution Failure: ${error.message}`);

            loadingState.classList.add("hidden");
            valuationForm.classList.remove("hidden");
        }
    });
});