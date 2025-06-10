import React, { useEffect, useState, useCallback } from 'react';
import {
  View,
  Text,
  FlatList,
  RefreshControl,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Linking,
} from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import Icon from 'react-native-vector-icons/MaterialIcons';

import { fetchHotArticles, refreshArticles } from '../store/slices/articlesSlice';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorMessage from '../components/ErrorMessage';
import { APP_CONFIG, ROUTES } from '../constants/config';

const HomeScreen = ({ navigation }) => {
  const dispatch = useDispatch();
  const { articles, isLoading, error, lastUpdated } = useSelector(state => state.articles);
  const { isAuthenticated } = useSelector(state => state.auth);
  
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    // 初始加载数据
    dispatch(fetchHotArticles());
  }, [dispatch]);

  const onRefresh = useCallback(async () => {
    setRefreshing(true);
    try {
      await dispatch(refreshArticles()).unwrap();
    } catch (error) {
      Alert.alert('刷新失败', error);
    } finally {
      setRefreshing(false);
    }
  }, [dispatch]);

  const handleArticlePress = (article) => {
    if (article.url) {
      navigation.navigate(ROUTES.WEB_VIEW, {
        url: article.url,
        title: article.title,
      });
    }
  };

  const handleAnalysisPress = () => {
    if (isAuthenticated) {
      navigation.navigate(ROUTES.ANALYSIS);
    } else {
      Alert.alert(
        '需要登录',
        '请先登录以访问数据分析功能',
        [
          { text: '取消', style: 'cancel' },
          { text: '登录', onPress: () => navigation.navigate(ROUTES.LOGIN) },
        ]
      );
    }
  };

  const renderArticleItem = ({ item, index }) => (
    <TouchableOpacity
      style={styles.articleItem}
      onPress={() => handleArticlePress(item)}
      activeOpacity={0.7}
    >
      <View style={styles.rankContainer}>
        <Text style={[
          styles.rankText,
          index < 3 && styles.topRankText
        ]}>
          {item.rank}
        </Text>
      </View>
      
      <View style={styles.contentContainer}>
        <Text style={styles.titleText} numberOfLines={2}>
          {item.title}
        </Text>
        
        {item.description && (
          <Text style={styles.descriptionText} numberOfLines={2}>
            {item.description}
          </Text>
        )}
        
        <View style={styles.metaContainer}>
          <View style={styles.metaItem}>
            <Icon name="whatshot" size={14} color={APP_CONFIG.THEME.ERROR_COLOR} />
            <Text style={styles.metaText}>{item.hot_value}</Text>
          </View>
          
          {item.answer_count > 0 && (
            <View style={styles.metaItem}>
              <Icon name="question-answer" size={14} color={APP_CONFIG.THEME.SECONDARY_TEXT_COLOR} />
              <Text style={styles.metaText}>{item.answer_count} 回答</Text>
            </View>
          )}
        </View>
      </View>
      
      <Icon name="chevron-right" size={20} color={APP_CONFIG.THEME.SECONDARY_TEXT_COLOR} />
    </TouchableOpacity>
  );

  const renderHeader = () => (
    <View style={styles.header}>
      <View style={styles.headerTop}>
        <Text style={styles.headerTitle}>知乎热榜</Text>
        <TouchableOpacity
          style={styles.refreshButton}
          onPress={onRefresh}
          disabled={refreshing}
        >
          <Icon 
            name="refresh" 
            size={24} 
            color={APP_CONFIG.THEME.PRIMARY_COLOR}
            style={refreshing && styles.rotating}
          />
        </TouchableOpacity>
      </View>
      
      {lastUpdated && (
        <Text style={styles.lastUpdated}>
          最后更新: {new Date(lastUpdated).toLocaleString()}
        </Text>
      )}
      
      {isAuthenticated && (
        <TouchableOpacity
          style={styles.analysisButton}
          onPress={handleAnalysisPress}
        >
          <Icon name="analytics" size={20} color="white" />
          <Text style={styles.analysisButtonText}>数据分析</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  if (isLoading && !articles.length) {
    return <LoadingSpinner message="加载热榜数据中..." />;
  }

  if (error && !articles.length) {
    return (
      <ErrorMessage
        message={error}
        onRetry={() => dispatch(fetchHotArticles())}
      />
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={articles}
        renderItem={renderArticleItem}
        keyExtractor={(item) => item.id.toString()}
        ListHeaderComponent={renderHeader}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[APP_CONFIG.THEME.PRIMARY_COLOR]}
            tintColor={APP_CONFIG.THEME.PRIMARY_COLOR}
          />
        }
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: APP_CONFIG.THEME.BACKGROUND_COLOR,
  },
  listContainer: {
    paddingBottom: APP_CONFIG.SPACING.LARGE,
  },
  header: {
    backgroundColor: APP_CONFIG.THEME.CARD_BACKGROUND,
    padding: APP_CONFIG.SPACING.MEDIUM,
    marginBottom: APP_CONFIG.SPACING.SMALL,
    elevation: 2,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: APP_CONFIG.SPACING.SMALL,
  },
  headerTitle: {
    fontSize: APP_CONFIG.FONT_SIZES.TITLE,
    fontWeight: 'bold',
    color: APP_CONFIG.THEME.TEXT_COLOR,
  },
  refreshButton: {
    padding: APP_CONFIG.SPACING.SMALL,
  },
  rotating: {
    transform: [{ rotate: '360deg' }],
  },
  lastUpdated: {
    fontSize: APP_CONFIG.FONT_SIZES.SMALL,
    color: APP_CONFIG.THEME.SECONDARY_TEXT_COLOR,
    marginBottom: APP_CONFIG.SPACING.SMALL,
  },
  analysisButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: APP_CONFIG.THEME.PRIMARY_COLOR,
    paddingVertical: APP_CONFIG.SPACING.SMALL,
    paddingHorizontal: APP_CONFIG.SPACING.MEDIUM,
    borderRadius: APP_CONFIG.BORDER_RADIUS.MEDIUM,
  },
  analysisButtonText: {
    color: 'white',
    fontSize: APP_CONFIG.FONT_SIZES.MEDIUM,
    fontWeight: '600',
    marginLeft: APP_CONFIG.SPACING.SMALL,
  },
  articleItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: APP_CONFIG.THEME.CARD_BACKGROUND,
    marginHorizontal: APP_CONFIG.SPACING.MEDIUM,
    marginVertical: APP_CONFIG.SPACING.SMALL / 2,
    padding: APP_CONFIG.SPACING.MEDIUM,
    borderRadius: APP_CONFIG.BORDER_RADIUS.MEDIUM,
    elevation: 1,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
  },
  rankContainer: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: APP_CONFIG.THEME.BACKGROUND_COLOR,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: APP_CONFIG.SPACING.MEDIUM,
  },
  rankText: {
    fontSize: APP_CONFIG.FONT_SIZES.MEDIUM,
    fontWeight: 'bold',
    color: APP_CONFIG.THEME.TEXT_COLOR,
  },
  topRankText: {
    color: APP_CONFIG.THEME.ERROR_COLOR,
  },
  contentContainer: {
    flex: 1,
  },
  titleText: {
    fontSize: APP_CONFIG.FONT_SIZES.MEDIUM,
    fontWeight: '600',
    color: APP_CONFIG.THEME.TEXT_COLOR,
    lineHeight: 20,
    marginBottom: APP_CONFIG.SPACING.SMALL,
  },
  descriptionText: {
    fontSize: APP_CONFIG.FONT_SIZES.SMALL,
    color: APP_CONFIG.THEME.SECONDARY_TEXT_COLOR,
    lineHeight: 16,
    marginBottom: APP_CONFIG.SPACING.SMALL,
  },
  metaContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  metaItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: APP_CONFIG.SPACING.MEDIUM,
  },
  metaText: {
    fontSize: APP_CONFIG.FONT_SIZES.SMALL,
    color: APP_CONFIG.THEME.SECONDARY_TEXT_COLOR,
    marginLeft: 4,
  },
});

export default HomeScreen;
