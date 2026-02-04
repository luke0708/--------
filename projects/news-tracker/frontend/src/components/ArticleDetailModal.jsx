import React, { useEffect } from "react";

export default function ArticleDetailModal({ article, onClose }) {
     if (!article) return null;

     // 监听 ESC 键关闭
     useEffect(() => {
          function handleKeyDown(e) {
               if (e.key === "Escape") onClose();
          }
          window.addEventListener("keydown", handleKeyDown);
          return () => window.removeEventListener("keydown", handleKeyDown);
     }, [onClose]);

     // 点击遮罩关闭
     const handleBackdropClick = (e) => {
          if (e.target === e.currentTarget) {
               onClose();
          }
     };

     return (
          <div className="modal-backdrop" onClick={handleBackdropClick}>
               <div className="modal-content">
                    <button className="modal-close-btn" onClick={onClose}>
                         ×
                    </button>

                    <div className="modal-header">
                         <h2>{article.title_zh || article.title_orig}</h2>
                         <div className="modal-meta">
                              <span className="source-tag">{article.source_name}</span>
                              <span className="date-tag">
                                   {article.published_at ? new Date(article.published_at).toLocaleString() : ""}
                              </span>
                         </div>
                    </div>

                    <div className="modal-body">
                         <div className="scores-section">
                              <div className="score-badge" title="金融评分 (0-1)">
                                   <span className="label">评分</span>
                                   <span className="value">{article.finance_score.toFixed(2)}</span>
                              </div>
                              <div className="score-badge" title="AI 相关性标签">
                                   <span className="label">标签</span>
                                   <span className="value">{article.relevance_label || "N/A"}</span>
                              </div>
                              {article.is_primary_lang && (
                                   <div className="score-badge primary-lang">
                                        <span className="value">主语言</span>
                                   </div>
                              )}
                         </div>

                         <div className="summary-section">
                              <h3>AI 摘要</h3>
                              <p className="summary-text">{article.summary_zh || "暂无中文摘要"}</p>
                         </div>

                         <div className="original-section">
                              <details>
                                   <summary>查看原文信息</summary>
                                   <div className="original-content">
                                        <h4>{article.title_orig}</h4>
                                        <p>{article.summary_orig || "No original summary available."}</p>
                                   </div>
                              </details>
                         </div>
                    </div>

                    <div className="modal-footer">
                         <a
                              href={article.url}
                              target="_blank"
                              rel="noreferrer"
                              className="btn-primary-link"
                         >
                              阅读原文 →
                         </a>
                    </div>
               </div>
          </div>
     );
}
