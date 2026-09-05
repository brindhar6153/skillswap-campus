package com.example.skillswapcampus.ui.skills

import com.example.skillswapcampus.models.Skill
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class SkillsFilterTest {

    private val testCatalog = listOf(
        Skill(1, "Java", "Programming Languages"),
        Skill(2, "Python", "Programming Languages"),
        Skill(3, "C++", "Programming Languages"),
        Skill(4, "React", "Web Development"),
        Skill(5, "Node.js", "Web Development"),
        Skill(6, "Flask", "Backend Development"),
        Skill(7, "Android Development", "Mobile Development"),
        Skill(8, "React Native", "Mobile Development"),
        Skill(9, "MySQL", "Databases"),
        Skill(10, "PostgreSQL", "Databases"),
        Skill(11, "Machine Learning", "AI & Machine Learning"),
        Skill(12, "Deep Learning", "AI & Machine Learning"),
        Skill(13, "Data Structures", "Data & Analytics"),
        Skill(14, "Git", "Software Development & Tools"),
        Skill(15, "AWS", "Cloud & DevOps"),
        Skill(16, "Cybersecurity", "Cybersecurity"),
        Skill(17, "Figma", "UI/UX & Design")
    )

    private val allCategoriesLabel = "All Categories"

    private fun filterSkills(
        skills: List<Skill>,
        searchQuery: String,
        selectedCategory: String
    ): List<Skill> {
        val query = searchQuery.trim()
        return skills.filter { skill ->
            val matchesCategory = (selectedCategory == allCategoriesLabel || selectedCategory == "All" || skill.category.equals(selectedCategory, ignoreCase = true))
            if (query.isNotEmpty()) {
                val matchesSearch = skill.name.contains(query, ignoreCase = true) || skill.category.contains(query, ignoreCase = true)
                matchesSearch && matchesCategory
            } else {
                matchesCategory
            }
        }
    }

    @Test
    fun testSearchJavaFindsJavaRegardlessOfPreviousCategory() {
        // Simulating user having "Data & Analytics" selected, then typing "java"
        var selectedCategory = "Data & Analytics"
        val newQuery = "java"
        if (newQuery.isNotBlank() && selectedCategory != allCategoriesLabel) {
            selectedCategory = allCategoriesLabel
        }

        val results = filterSkills(testCatalog, newQuery, selectedCategory)
        assertEquals(1, results.size)
        assertEquals("Java", results[0].name)
        assertEquals("Programming Languages", results[0].category)
    }

    @Test
    fun testSearchPythonFindsPython() {
        val results = filterSkills(testCatalog, "python", allCategoriesLabel)
        assertEquals(1, results.size)
        assertEquals("Python", results[0].name)
    }

    @Test
    fun testSearchReactFindsReactAndReactNative() {
        val results = filterSkills(testCatalog, "react", allCategoriesLabel)
        assertEquals(2, results.size)
        assertTrue(results.any { it.name == "React" })
        assertTrue(results.any { it.name == "React Native" })
    }

    @Test
    fun testSearchMySQLFindsMySQL() {
        val results = filterSkills(testCatalog, "mysql", allCategoriesLabel)
        assertEquals(1, results.size)
        assertEquals("MySQL", results[0].name)
        assertEquals("Databases", results[0].category)
    }

    @Test
    fun testSearchMachineLearningFindsMachineLearning() {
        val results = filterSkills(testCatalog, "machine learning", allCategoriesLabel)
        assertTrue(results.any { it.name == "Machine Learning" })
    }

    @Test
    fun testCategoryFilterWithoutSearch() {
        val results = filterSkills(testCatalog, "", "Databases")
        assertEquals(2, results.size)
        assertTrue(results.all { it.category == "Databases" })
    }

    @Test
    fun testClearingSearchRestoresAllOrSelectedCategory() {
        val resultsAll = filterSkills(testCatalog, "", allCategoriesLabel)
        assertEquals(testCatalog.size, resultsAll.size)

        val resultsMobile = filterSkills(testCatalog, "", "Mobile Development")
        assertEquals(2, resultsMobile.size)
    }
}
