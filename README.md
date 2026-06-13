# Multimodal Industrial Scrap Valuation Platform

An asynchronous, production-grade AI platform that fuses **Computer Vision (Deep Learning)** and **Natural Language Processing (NLP)** to deliver real-time asset pricing valuations for industrial scrap streams. 

Live Demo Link: 

---

##  Key Architectural Highlights 

* **Multimodal Feature Fusion:** Instead of running isolated predictions, the platform applies an late-fusion architecture—horizontally stacking a **1280-dimensional visual embedding vector** (extracted via Transfer Learning) with **token-mapped tabular properties** parsed from messy user text descriptions.
* **Production ASGI Performance:** Built on **FastAPI** leveraging asynchronous non-blocking routing paradigms to process multi-part digital file uploads and metadata concurrently under **200ms**.
* **Enterprise Grade Model Persistence:** Deep learning weights and classical regression models are cached natively into memory at server initialization, eliminating disk I/O overhead on subsequent inference API requests.

---

## 🛠️ System Architecture Diagram

```text
                  ┌────────────────────────────────────────┐
                  │          Beautiful Home Page           │
                  │       (HTML5 + Tailwind CSS via CDN)    │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼  [Async Form Payload: Text + Image]
                  ┌────────────────────────────────────────┐
                  │             FastAPI Backend            │
                  └───────────────────┬────────────────────┘
                                      │
           ┌──────────────────────────┴──────────────────────────┐
           ▼ (NLP Processing)                                    ▼ (Computer Vision Engine)
┌─────────────────────────────────────┐               ┌─────────────────────────────────────┐
│ 1. Text Normalization               │               │ 1. Raw Stream Vectorization         │
│    (Case Insensitive Tokenization)  │               │    (In-memory PIL Conversion)       │
│ 2. Custom Regex Pattern Extractor   │               │ 2. Transfer Learning Feature Net    │
│    (Isolates weights via Regex maps)│               │    (Frozen MobileNetV2 Base)        │
│ 3. Category Mapping Layer            │               │ 3. Spatial Matrix Compression       │
│    (Matches multi-lingual slang)    │               │    (Global Average Pooling 2D)      │
└──────────────────┬──────────────────┘               └──────────────────┬──────────────────┘
                   │                                                     │
                   │           ┌─────────────────────────────┐           │
                   └──────────►│  NumPy Horizontal Stacking  ├───────────┘
                               │   (Multimodal Late Fusion)  │
                               └──────────────┬──────────────┘
                                              │
                                              ▼ [Fused Feature Array]
                               ┌─────────────────────────────┐
                               │   Random Forest Regressor   │
                               │  (Non-Linear Valuation Engine)│
                               └──────────────┬──────────────┘
                                              │
                                              ▼ [200 OK Response]
                               ┌─────────────────────────────┐
                               │   JSON Package + Confidence  │
                               │   Boundaries Matrix (₹ Range)│
                               └─────────────────────────────┘