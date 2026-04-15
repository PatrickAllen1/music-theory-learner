import { useState } from "react";

const KEY = "mtl-progress";

function load() {
  try {
    return JSON.parse(localStorage.getItem(KEY)) || {};
  } catch {
    return {};
  }
}

export function useProgress() {
  const [progress, setProgress] = useState(load);

  const markStep = (buildId, stepId) => {
    setProgress((prev) => {
      const next = {
        ...prev,
        [buildId]: { ...prev[buildId], [stepId]: true },
      };
      localStorage.setItem(KEY, JSON.stringify(next));
      return next;
    });
  };

  const unmarkStep = (buildId, stepId) => {
    setProgress((prev) => {
      const next = { ...prev, [buildId]: { ...prev[buildId] } };
      delete next[buildId][stepId];
      localStorage.setItem(KEY, JSON.stringify(next));
      return next;
    });
  };

  const stepsComplete = (buildId) =>
    Object.keys(progress[buildId] || {}).length;

  const isBuildComplete = (build) =>
    stepsComplete(build.id) >= build.steps.length;

  const isStepComplete = (buildId, stepId) =>
    !!(progress[buildId] && progress[buildId][stepId]);

  return {
    progress,
    markStep,
    unmarkStep,
    stepsComplete,
    isBuildComplete,
    isStepComplete,
  };
}
