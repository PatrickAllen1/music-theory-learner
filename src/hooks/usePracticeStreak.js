import { useState } from "react";

const KEY = "mtl-streak";

function today() {
  return new Date().toISOString().slice(0, 10); // YYYY-MM-DD
}

function load() {
  try {
    return (
      JSON.parse(localStorage.getItem(KEY)) || {
        lastDate: null,
        streak: 0,
        completedToday: [],
      }
    );
  } catch {
    return { lastDate: null, streak: 0, completedToday: [] };
  }
}

function save(data) {
  localStorage.setItem(KEY, JSON.stringify(data));
}

export function usePracticeStreak() {
  const [streakData, setStreakData] = useState(load);

  // Call when a build is opened — records practice for today and updates streak
  const recordPractice = () => {
    setStreakData((prev) => {
      const t = today();
      if (prev.lastDate === t) return prev; // already recorded today

      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yStr = yesterday.toISOString().slice(0, 10);

      const newStreak = prev.lastDate === yStr ? prev.streak + 1 : 1; // consecutive = extend, else reset to 1

      const next = { ...prev, lastDate: t, streak: newStreak };
      save(next);
      return next;
    });
  };

  const markCompleted = (buildId) => {
    setStreakData((prev) => {
      if (prev.completedToday.includes(buildId)) return prev;
      const next = {
        ...prev,
        completedToday: [...prev.completedToday, buildId],
      };
      save(next);
      return next;
    });
  };

  const practicedToday = streakData.lastDate === today();

  return {
    streak: streakData.streak,
    practicedToday,
    completedToday: streakData.completedToday,
    recordPractice,
    markCompleted,
  };
}
